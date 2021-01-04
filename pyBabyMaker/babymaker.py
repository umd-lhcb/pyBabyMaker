#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Mon Jan 04, 2021 at 01:54 AM +0100

import re

from pyBabyMaker.base import TermColor as TC
from pyBabyMaker.base import UniqueList, BaseMaker, Variable
from pyBabyMaker.base import update_config
from pyBabyMaker.boolean.utils import find_all_vars
from pyBabyMaker.engine.core import template_transformer, template_evaluator


###########
# Helpers #
###########

# We need some global thing to track all variable names to avoid name collision

# We need to load the calculation stuff first given that we have only one
# tracker for their name

# For other output branch, we can rename them on the fly

# Variables

# Just use dictionary as namespaces man! Don't try to resolve them!

# So we need to keep an record on the name of output branches!


class ParsedExpr:
    pass


########################
# Configuration parser #
########################

class BabyConfigParser:
    """
    Basic parser for YAML C++ code instruction.
    """
    def __init__(self, parsed_config, dumped_ntuple, debug=False):
        """
        Initialize the config parser with parsed YAML file and dumped ntuple
        structure.
        """
        self.parsed_config = parsed_config
        self.dumped_ntuple = dumped_ntuple
        self.debug = debug

    # NOTE: A complicated function! I'd like it to be more elegant but not for
    #       now
    def parse(self):
        """
        Parse the loaded YAML dict (in ``self.parsed_config``) and dumped ntuple
        tree structure (in ``self.dumped_ntuple``).
        """
        directive = {
            'system_headers': UniqueList(),
            'user_headers': UniqueList(),
            'trees': {},
        }

        self.parse_headers(self.parsed_config, directive)

        for output_tree, config in self.parsed_config['output'].items():
            input_tree = config['input']

            try:
                dumped_tree = self.dumped_ntuple[input_tree]
            except KeyError:
                print('{}Input tree {} not found, skipping {}...{}'.format(
                    TC.BOLD+TC.YELLOW, input_tree, output_tree, TC.END
                ))
                continue

            print('{}=== Handling output tree {} ==={}'.format(
                TC.BOLD+TC.BLUE, output_tree, TC.END))

            # Merge raw tree-specific directive with the global one.
            merge = config['inherit'] if 'inherit' in config else True
            config = update_config(self.parsed_config, config, merge=merge)
            subdirective = {'input_tree': input_tree, 'namespace': {}}

            # Find output branches, without resolving dependency.
            self.parse_drop_keep_rename(config, dumped_tree, subdirective)
            self.parse_calculation(config, subdirective)

            # Figure out the loading sequence of all variables, resolving
            # dependency issues.
            subdirective['known_names'] += [
                v.name for v in subdirective['input_branches']]
            vars_to_load = subdirective['output_branches'] + \
                subdirective['temp_variables']

            transient_vars, vars_to_load = self.var_load_seq(
                vars_to_load, dumped_tree, subdirective)

            # Remove variables that can't be resolved
            for var in vars_to_load:
                if var in subdirective['output_branches']:
                    print("{}Output branch {} cannot be resolved, deleting...{}".format(
                        TC.YELLOW, var.name, TC.END))
                    subdirective['output_branches'].remove(var)
                else:
                    print("{}Temp variable {} cannot be resolved, deleting...{}".format(
                        TC.YELLOW, var.name, TC.END))
                    subdirective['temp_variables'].remove(var)

            self.parse_selection(config, dumped_tree, subdirective)

            subdirective['input_branch_names'] = [
                v.name for v in subdirective['input_branches']]

            # Consider variable loaded if exactly the same name is in the input
            # branches.
            subdirective['transient_vars'] = [
                v for v in transient_vars
                if v.name not in subdirective['input_branch_names']]

            directive['trees'][output_tree] = subdirective

        return directive

    @staticmethod
    def parse_headers(config, directive):
        """
        Parse ``headers`` section.
        """
        for header_type in ('system', 'user'):
            if 'headers' in config and header_type in config['headers']:
                directive['{}_headers'.format(header_type)] += \
                    config['headers'][header_type]

    @classmethod
    def parse_drop_keep_rename(cls, config, dumped_tree, subdirective):
        """
        Parse ``drop, keep, rename`` sections.
        """
        for br, datatype in dumped_tree.items():
            if 'drop' in config and cls.match(config['drop'], br):
                print('Dropping branch: {}'.format(br))
                continue

            for section in ('keep', 'rename'):
                if section in config and cls.match(config[section], br):
                    subdirective['namespace'][section][br] = \
                        Variable(datatype, br)

    @classmethod
    def parse_calculation(cls, config, subdirective):
        """
        Parse ``calculation`` section.
        """
        if 'calculation' in config:
            for name, code in config['calculation'].items():
                splitted = code.split(';')
                try:
                    datatype, rvalue, rvalue_alt = splitted
                except ValueError:
                    try:
                        datatype, rvalue = code.splitted
                        rvalue_alt = None
                    except ValueError:
                        raise ValueError('Illegal specification for {}: {}.'.format(
                            name, code
                        ))

                if '^' in datatype:
                    subdirective['calculation'].append(Variable(
                        datatype.strip('^'), name, rvalue, rvalue_alt, True))
                else:
                    subdirective['calculation'].append(Variable(
                        datatype, name, rvalue, rvalue_alt))

    def parse_selection(self, config, dumped_tree, directive):
        """
        Parse ``selection`` section.
        """
        if 'selection' in config:
            selection = []

            for expr in config['selection']:
                resolved = self.load_missing_vars(expr, dumped_tree, directive)
                if resolved:
                    selection.append(expr)
                else:
                    print('{}Selection {} not resolved, deleting...{}'.format(
                        TC.YELLOW, expr, TC.END))

            directive['selection'] = selection

    def load_missing_vars(self, expr, dumped_tree, directive):
        """
        Load missing variables required for calculation or comparison, provided
        that the variables are available directly in the ntuple.
        """
        variables = UniqueList(find_all_vars(expr))
        resolved = True

        for v in variables:
            if v not in directive['known_names']:
                try:
                    datatype = self.load_var(v, dumped_tree)
                    directive['input_branches'].append(Variable(datatype, v))
                    directive['known_names'].append(v)

                except Exception:
                    if self.debug:
                        print('{} is not a known branch name.'.format(v))
                    resolved = False

        return resolved

    def var_load_seq(self, vars_to_load, dumped_tree, directive,
                     transient_vars=None,
                     cur_iter=0, max_iter=5):
        """
        Figure out a load sequence for ``vars_to_load`` such that variables that
        load later do not depend on variables loaded earlier.
        """
        transient_vars = [] if transient_vars is None else transient_vars
        known_names = directive['known_names']
        remain_vars_to_load = []

        if cur_iter < max_iter:
            for var in vars_to_load:
                resolved = self.load_missing_vars(var.rvalue,
                                                  dumped_tree, directive)
                if resolved:
                    transient_vars.append(var)
                    known_names.append(var.name)
                else:
                    remain_vars_to_load.append(var)

            if remain_vars_to_load:
                return self.var_load_seq(remain_vars_to_load, dumped_tree,
                                         directive, transient_vars,
                                         cur_iter+1, max_iter)

            return transient_vars, remain_vars_to_load
        # This is only triggered when no more iteration permitted yet we still
        # have unresolved variables.
        return transient_vars, vars_to_load

    @staticmethod
    def match(patterns, string, return_value=True):
        """
        Test if ``string`` matches at least one element in the ``patterns`` (a
        list of regular expression).

        If there's a match, return ``return_value``.
        """
        for p in patterns:
            if bool(re.search(r'{}'.format(p), string)):
                return return_value
        return not return_value

    @staticmethod
    def load_var(name, dumped_tree):
        """
        Load variable ``name`` from ntuple, if it's available.
        """
        try:
            datatype = dumped_tree[name]
            return datatype
        except KeyError:
            raise KeyError('Branch {} not found.'.format(name))


#############
# BabyMaker #
#############

class BabyMaker(BaseMaker):
    """
    ``babymaker`` class to glue parser and code generator together.
    """
    def __init__(self, config_filename, ntuple_filename, template_filename,
                 use_reformater=True):
        """
        Initialize with path to YAML file and ntuple file.
        """
        self.config_filename = config_filename
        self.ntuple_filename = ntuple_filename
        self.template_filename = template_filename
        self.use_reformater = use_reformater

    def gen(self, filename, debug=False):
        parsed_config = self.read(self.config_filename)
        dumped_ntuple = self.dump(self.ntuple_filename)
        directive = self.directive_gen(parsed_config, dumped_ntuple, debug)

        with open(self.template_filename) as tmpl:
            macros = template_transformer(tmpl, directive)

        output_cpp = template_evaluator(macros)

        with open(filename, 'w') as f:
            f.write(''.join(output_cpp))
        if self.use_reformater:
            self.reformat(filename)

    @staticmethod
    def directive_gen(parsed_config, dumped_ntuple, debug=False):
        parser = BabyConfigParser(parsed_config, dumped_ntuple, debug)
        return parser.parse()
