#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Tue Sep 22, 2020 at 02:33 AM +0800

import re

from pyBabyMaker.base import TermColor as TC
from pyBabyMaker.base import UniqueList, BaseMaker, Variable
from pyBabyMaker.base import update_config
from pyBabyMaker.boolean.utils import find_all_vars
from pyBabyMaker.engine.core import template_transformer, template_evaluator


########################
# Configuration parser #
########################

class BabyConfigParser:
    """
    Basic parser for YAML C++ code instruction.
    """
    def __init__(self, parsed_config, dumped_ntuple):
        """
        Initialize the config parser with parsed YAML file and dumped ntuple
        structure.
        """
        self.parsed_config = parsed_config
        self.dumped_ntuple = dumped_ntuple

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
            dumped_tree = self.dumped_ntuple[input_tree]
            print('{}=== Handling output tree {} ==={}'.format(
                TC.BOLD+TC.BLUE, output_tree, TC.END))

            # Merge raw tree-specific directive with the global one.
            merge = config['inherit'] if 'inherit' in config else True
            update_config(config, self.parsed_config, merge=merge)

            subdirective = self.gen_subdirective(input_tree)
            update_config(subdirective, config, merge=merge)

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

    def parse_headers(self, config, directive):
        """
        Parse ``headers`` section.
        """
        for header_type in ('system', 'user'):
            if 'headers' in config and header_type in config['headers']:
                directive['{}_headers'.format(header_type)] += \
                    config['headers'][header_type]

    def parse_drop_keep_rename(self, config, dumped_tree, directive):
        """
        Parse ``drop, keep, rename`` sections.
        """
        branches_to_keep = UniqueList()
        for br_in, datatype in dumped_tree.items():
            if 'drop' in config and self.match(config['drop'], br_in):
                print('Dropping branch: {}'.format(br_in))

            elif 'keep' in config and self.match(config['keep'], br_in) or \
                    'rename' in config and br_in in config['rename']:
                branches_to_keep.append((datatype, br_in))

        for datatype, br_in in branches_to_keep:
            directive['input_branches'].append(Variable(datatype, br_in))
            try:
                # Handle possible branch rename here
                br_out = config['rename'][br_in]
            except KeyError:
                br_out = br_in

            directive['output_branches'].append(
                Variable(datatype, br_out, br_in))

    def parse_calculation(self, config, directive):
        """
        Parse ``calculation`` section.
        """
        if 'calculation' in config:
            for name, code in config['calculation'].items():
                try:
                    datatype, rvalue = code.split(';')
                except ValueError:
                    raise ValueError('Illegal specification for {}: {}.'.format(
                        name, code
                    ))

                if '^' in datatype:
                    datatype = datatype.strip('^')
                    directive['temp_variables'].append(
                        Variable(datatype, name, rvalue))

                else:
                    directive['output_branches'].append(
                        Variable(datatype, name, rvalue))

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
    def gen_subdirective(input_tree):
        return {'input_tree': input_tree,
                'input_branches': UniqueList(),
                'output_branches': UniqueList(),
                'temp_variables': UniqueList(),
                'known_names': UniqueList(),
                'selection': ['true'],
                }

    @staticmethod
    def match(patterns, string, return_value=True):
        """
        Test if ``string`` (a regular expression) matches at least one element
        in the ``patterns``. If there's a match, return ``return_value``.
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

    def gen(self, filename):
        parsed_config = self.read(self.config_filename)
        dumped_ntuple = self.dump(self.ntuple_filename)
        directive = self.directive_gen(parsed_config, dumped_ntuple)

        with open(self.template_filename) as tmpl:
            macros = template_transformer(tmpl, directive)

        output_cpp = template_evaluator(macros)

        with open(filename, 'w') as f:
            f.write(''.join(output_cpp))
        if self.use_reformater:
            self.reformat(filename)

    @staticmethod
    def directive_gen(parsed_config, dumped_ntuple):
        parser = BabyConfigParser(parsed_config, dumped_ntuple)
        return parser.parse()
