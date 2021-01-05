#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Tue Jan 05, 2021 at 02:15 AM +0100

import re

from collections import namedtuple, defaultdict

from pyBabyMaker.base import TermColor as TC
from pyBabyMaker.base import UniqueList, BaseMaker
from pyBabyMaker.base import update_config
from pyBabyMaker.boolean.utils import find_all_vars
from pyBabyMaker.engine.core import template_transformer, template_evaluator


###########
# Helpers #
###########

class Variable(object):
    """
    Store input/output/transient variable to be resolved.

    **Note**: ``transient`` here means the variable **DOES NOT** exist in the
    input ntuple tree and thus went through some more complex transformation (
    i.e. renaming or calculation).
    """
    def __init__(self, type, name,
                 rvalue=None, rvalue_alt=None, transient=False, output=True):
        self.type = type
        self.name = name
        self.rvalue = rvalue
        self.rvalue_alt = rvalue_alt
        self.transient = transient
        self.output = output

        self.resolved_vars = {}
        self.counter = 0  # This holds counters to attempts to resolve this

        self.dep_vars = UniqueList(find_all_vars(rvalue)) \
            if rvalue is not None else []
        self.dep_vars_alt = UniqueList(find_all_vars(rvalue_alt)) \
            if rvalue_alt is not None else []

        self.to_resolve_expr = rvalue
        self.to_resolve_deps = self.dep_vars

    def use_alt(self):
        self.reset_counter()
        self.to_resolve_expr = self.rvalue_alt
        self.to_resolve_deps = self.dep_vars_alt
        return self

    def reset_counter(self):
        self.counter = 0

    def expr(self):
        expr = self.to_resolve_expr
        for orig, resolved in self.resolved_vars.items():
            expr = re.sub(r'\b'+orig+r'\b', resolved, expr)
        return expr

    def __eq__(self, other):
        if isinstance(other, Variable):
            return (self.type == other.type and self.name == other.name and
                    self.rvalue == other.rvalue and
                    self.rvalue_alt == other.rvalue_alt and
                    self.transient == other.transient and
                    self.output == other.output)
        return False


VariableResolved = namedtuple('VariableResolved',
                              'type name rvalue, branch_name',
                              defaults=(None, None))


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
            namespace = defaultdict(dict)
            namespace['raw'] = {n: Variable(t, n)
                                for n, t in dumped_tree.items()}
            subdirective = {
                'input_tree': input_tree,
                'namespace': namespace,
                'loaded_vars': [],
                'input_branches': [],
                'output_branches': [],
                'transient_vars': [],
                'input_branch_names': [],
                'output_branch_names': []
            }

            # Put all variables in separate namespaces
            self.parse_drop_keep_rename(config, subdirective)
            self.parse_calculation(config, subdirective)

            # Now resolve variable names for simple 'keep' and 'rename' actions
            self.resolve_vars_in_scope(
                'keep', subdirective['namespace']['keep'], subdirective)
            self.resolve_vars_in_scope(
                'rename', subdirective['namespace']['rename'], subdirective)

            # Figure out the loading sequence of all variables, resolving
            # dependency issues.
            unresolved = self.resolve_vars_in_scope(
                'calculation', subdirective['namespace']['calculation'],
                subdirective, ['keep', 'rename'])

            # Remove variables that can't be resolved
            for var in unresolved:
                if var.output:
                    print("{}Output branch {} cannot be resolved...{}".format(
                        TC.YELLOW, var.name, TC.END))
                else:
                    print("{}Temp variable {} cannot be resolved...{}".format(
                        TC.YELLOW, var.name, TC.END))

            # self.parse_selection(config, dumped_tree, subdirective)

            subdirective['input_branch_names'] = [
                v.name for v in subdirective['input_branches']]

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
    def parse_drop_keep_rename(cls, config, subdirective):
        """
        Parse ``drop, keep, rename`` sections.
        """
        if 'rename' in config:
            rename_dict = config['rename']
            rename_vars = list(rename_dict.keys())

        for var in subdirective['namespace']['raw'].values():
            if 'drop' in config and cls.match(config['drop'], var.name):
                print('Dropping branch: {}'.format(var.name))
                continue

            elif 'keep' in config and cls.match(config['keep'], var.name):
                subdirective['namespace']['keep'][var.name] = Variable(
                    var.type, var.name, var.name)

            elif 'rename' in config and cls.match(rename_vars, var.name):
                renamed_var = rename_dict[var.name]
                subdirective['namespace']['rename'][renamed_var] = Variable(
                    var.type, renamed_var, var.name, transient=True)

    @staticmethod
    def parse_calculation(config, subdirective):
        """
        Parse ``calculation`` section.
        """
        if 'calculation' in config:
            for name, code in config['calculation'].items():
                splitted = code.split(';')
                if len(splitted) == 3:
                    datatype, rvalue, rvalue_alt = splitted
                elif len(splitted) == 2:
                    datatype, rvalue = splitted
                    rvalue_alt = None
                else:
                    raise ValueError('Illegal specification for {}: {}.'.format(
                        name, code
                    ))

                output = True
                if '^' in datatype:
                    datatype = datatype.strip('^')
                    output = False

                subdirective['namespace']['calculation'][name] = Variable(
                    datatype, name, rvalue, rvalue_alt, True, output)

    def parse_selection(self, config, dumped_tree, directive):
        """
        Parse ``selection`` section.
        """
        # if 'selection' in config:
        #     selection = []

        #     for expr in config['selection']:
        #         resolved = self.load_missing_vars(expr, dumped_tree, directive)
        #         if resolved:
        #             selection.append(expr)
        #         else:
        #             print('{}Selection {} not resolved, deleting...{}'.format(
        #                 TC.YELLOW, expr, TC.END))

        #     directive['selection'] = selection

    @classmethod
    def resolve_vars_in_scope(cls, scope, variables, subdirective,
                              allowed_scopes=[], max_counter=5):
        unresolved = {}
        for var in variables.values():
            if not cls.resolve_var(scope, var, subdirective,
                                   allowed_scopes):
                unresolved[var.name] = var

        if len(unresolved) > 0 and unresolved[0].counter <= max_counter:
            return cls.resolve_vars_in_scope(
                scope, unresolved, subdirective, allowed_scopes, max_counter)

        return unresolved

    @staticmethod
    def resolve_var(scope, var, subdirective, allowed_scopes):
        """
        Resolve variable names within allowed scoped or vanilla ntuple trees.
        """
        def resolve_in_scope(
            s, namespace=subdirective['namespace'],
            loaded=lambda x: x in subdirective['loaded_vars'], terminal=False
        ):
            remainder = []
            for v in var.to_resolve_deps:
                if s == scope and v == var.name:
                    remainder.append(v)
                    continue  # No self-referencing allowed!

                v_resolved = s + '_' + v
                if v in namespace[s] and loaded(v_resolved):
                    var.resolved_vars[v] = v_resolved
                    if terminal:
                        subdirective['input_branches'].append(
                            VariableResolved(namespace[s][v], v_resolved))
                        subdirective['loaded_vars'].append(v_resolved)

                else:
                    remainder.append(v)
            var.to_resolve_deps = remainder

        for s in allowed_scopes+[scope]:
            resolve_in_scope(s)

        # As a last resort, load from ntuple trees
        resolve_in_scope('raw', loaded=lambda x: True, terminal=True)

        if not len(var.to_resolve_deps):
            var_resolved = scope + '_' + var.name
            subdirective['loaded_vars'].append(var_resolved)
            if var.transient:
                subdirective['transient_vars'].append(VariableResolved(
                    var.type, var_resolved, var.expr()))
            if var.output:
                subdirective['output_branches'].append(VariableResolved(
                    var.type, var_resolved, var.expr(), var.name))
                # Check if we have duplicated output branch name
                if var.name in subdirective['output_branch_names']:
                    raise ValueError('{}Redefinition of output branch {} in scope {}!{}'.format(
                        TC.BOLD+TC.RED, var.name, scope, TC.END
                    ))
                else:
                    subdirective['output_branch_names'].append(var.name)

        var.counter += 1
        return not bool(len(var.to_resolve_deps))

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
