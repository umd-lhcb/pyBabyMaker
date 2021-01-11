#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Mon Jan 11, 2021 at 03:14 AM +0100

import re

from collections import namedtuple, defaultdict

from pyBabyMaker.base import TermColor as TC
from pyBabyMaker.base import UniqueList, BaseMaker
from pyBabyMaker.base import update_config
from pyBabyMaker.engine.core import template_transformer, template_evaluator
from pyBabyMaker.var_resolver import VariableResolver


###########
# Helpers #
###########

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
                'temp_vars': [],
                'simple_vars': [],
                'input_branch_names': [],
                'output_branch_names': [],
                'selection': ['true'],
            }

            # Put all variables in separate namespaces
            self.parse_drop_keep_rename(config, subdirective)
            self.parse_calculation(config, subdirective)

            # Now resolve variable names for simple 'keep' and 'rename' actions
            self.resolve_vars_in_scope(
                'keep', subdirective['namespace']['keep'], subdirective)
            self.resolve_vars_in_scope(
                'rename', subdirective['namespace']['rename'], subdirective)

            # Resolve variables in 'calculation'
            unresolved = self.resolve_vars_in_scope(
                'calculation', subdirective['namespace']['calculation'],
                subdirective, ['rename'])

            # Try to switch to alternative expression for unresolved variables
            [v.use_alt() for v in unresolved.values()]
            unresolved = self.resolve_vars_in_scope(
                'calculation', unresolved, subdirective, ['rename'])

            # Remove variables that can't be resolved
            for var in unresolved.values():
                if var.output:
                    print("{}Output branch {} cannot be resolved...{}".format(
                        TC.YELLOW, var.name, TC.END))
                else:
                    print("{}Temp variable {} cannot be resolved...{}".format(
                        TC.YELLOW, var.name, TC.END))

            self.parse_selection(config, subdirective)

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

            if 'rename' in config and cls.match(rename_vars, var.name):
                renamed_var = rename_dict[var.name]
                subdirective['namespace']['rename'][renamed_var] = Variable(
                    var.type, renamed_var, var.name, transient=True)
                continue

            if 'keep' in config and cls.match(config['keep'], var.name):
                subdirective['namespace']['keep'][var.name] = Variable(
                    var.type, var.name, var.name)

    @staticmethod
    def parse_calculation(config, subdirective):
        """
        Parse ``calculation`` section.
        """
        if 'calculation' in config:
            for name, code in config['calculation'].items():
                splitted = [i.strip() for i in code.split(';')]
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

    @classmethod
    def parse_selection(cls, config, subdirective):
        """
        Parse ``selection`` section.
        """
        if 'selection' in config:
            for expr in config['selection']:
                virtual_var = Variable(None, 'sel', expr, output=False)
                resolved = cls.resolve_var(
                    'selection', virtual_var, subdirective,
                    ['calculation', 'rename'])
                if resolved:
                    subdirective['selection'].append(virtual_var.expr())
                else:
                    print('{}Selection {} not resolved, deleting...{}'.format(
                        TC.YELLOW, expr, TC.END))

    @classmethod
    def resolve_vars_in_scope(cls, scope, variables, subdirective,
                              allowed_scopes=[], max_counter=5):
        unresolved = {}
        for var in variables.values():
            if not cls.resolve_var(scope, var, subdirective,
                                   allowed_scopes):
                unresolved[var.name] = var

        if len(unresolved) > 0 and \
                next(iter(unresolved.values())).counter <= max_counter:
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
                elif v in namespace[s] and terminal:
                    var.resolved_vars[v] = v_resolved
                    subdirective['input_branches'].append(
                        VariableResolved(
                            namespace[s][v].type, v_resolved, None, v))
                    subdirective['loaded_vars'].append(v_resolved)
                else:
                    remainder.append(v)
            var.to_resolve_deps = remainder

        if var.to_resolve_deps is False:  # Don't resolve if dependency is nil
            var.counter += 1
            return False

        for s in allowed_scopes+[scope]:
            resolve_in_scope(s)

        # As a last resort, load from ntuple trees
        resolve_in_scope('raw', terminal=True)

        if not len(var.to_resolve_deps):
            var_resolved = scope + '_' + var.name
            subdirective['loaded_vars'].append(var_resolved)

            if var.transient:
                _var = VariableResolved(var.type, var_resolved, var.expr())
                subdirective['transient_vars'].append(_var)
                if not var.output:
                    subdirective['temp_vars'].append(_var)

            if var.output:
                _var = VariableResolved(
                    var.type, var_resolved, var.expr(), var.name)
                subdirective['output_branches'].append(_var)
                # Check if we have duplicated output branch name
                if var.name in subdirective['output_branch_names']:
                    raise ValueError('{}Redefinition of output branch {} in scope {}!{}'.format(
                        TC.BOLD+TC.RED, var.name, scope, TC.END
                    ))
                else:
                    subdirective['output_branch_names'].append(var.name)
                if not var.transient:
                    subdirective['simple_vars'].append(_var)

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
