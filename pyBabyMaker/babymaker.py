#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Wed Jan 13, 2021 at 12:30 AM +0100

import re
import logging

from collections import defaultdict
from dataclasses import dataclass

from pyBabyMaker.base import TermColor as TC
from pyBabyMaker.base import UniqueList, BaseMaker
from pyBabyMaker.base import update_config
from pyBabyMaker.engine.core import template_transformer, template_evaluator
from pyBabyMaker.var_resolver import Variable, VariableResolver


###########
# Helpers #
###########

@dataclass
class BabyVariable(Variable):
    """
    Store both raw variables and resolved variables.

    The added attributes make sorting variables easier.
    """
    input: bool = False
    output: bool = True
    fake: bool = False

    def __post_init__(self):
        super().__post_init__()
        self._fname = self.name  # 'fname' -> full name
        self.fname_set = False

    def __repr__(self):
        return super().__repr__()

    @property
    def fname(self):
        return self._fname

    @fname.setter
    def fname(self, fname):
        if not self.fname_set:
            self.fname_set = True
            self._fname = fname


class BabyVariableResolver(VariableResolver):
    @staticmethod
    def format_resolved(scope, var):
        """
        Prepare resolved variables for ``babymaker``.
        """
        var.fname = scope+'_'+var.name
        return var


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

        if debug:
            logging.basicConfig(level=logging.DEBUG)
            self._resolvers = []

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
            namespace['raw'] = {n: BabyVariable(n, t, input=True, output=False)
                                for n, t in dumped_tree.items()}

            # Load all variables in separate namespaces
            self.parse_drop_keep_rename(config, namespace)
            self.parse_calculation(config, namespace)
            self.parse_selection(config, namespace)

            # Initialize a variable resolver
            resolver = BabyVariableResolver(namespace)
            if self.debug:
                self._resolvers.append(resolver)

            # Resolve variables needed for selection
            selection, unresolved_selection = resolver.resolve_scope(
                'selection', ['calculation', 'rename', 'raw'])

            # Resolve all other variables
            keep, unresolved_keep = resolver.resolve_scope('keep', ['raw'])
            rename, unresolved_rename = resolver.resolve_scope(
                'rename', ['raw'])
            calculation, unresolved_calculation = resolver.resolve_scope(
                'calculation', ['calculation', 'rename', 'raw'])
            resolved_vars = selection + keep + rename + calculation
            most_unresolved_vars = unresolved_keep + unresolved_rename + \
                unresolved_calculation

            # Remove variables that can't be resolved
            for var in most_unresolved_vars:
                if var.output:
                    print("{}Output branch {} cannot be resolved...{}".format(
                        TC.YELLOW, var.name, TC.END))
                else:
                    print("{}Temp variable {} cannot be resolved...{}".format(
                        TC.YELLOW, var.name, TC.END))

            for var in unresolved_selection:
                print("{}Selection expr {} cannot be resolved...{}".format(
                    TC.YELLOW, var.rval, TC.END))

            directive['trees'][output_tree] = {
                'input_tree': input_tree,
                'sel': ['true'] + [v.rval for v in selection if v.fake],
                'pre_sel_vars':
                [v for v in selection if not v.fake and not v.input],
                'post_sel_vars':
                [v for v in keep+rename+calculation
                 if not v.fake and not v.input],
                'input': [v for v in resolved_vars if v.input],
                'output': [v for v in resolved_vars if v.output],
                'tmp':
                [v for v in resolved_vars
                 if True not in [v.input, v.output, v.fake]],
                'input_br': [v.fname for v in resolved_vars if v.input],
            }

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
    def parse_drop_keep_rename(cls, config, namespace):
        """
        Parse ``drop, keep, rename`` sections.
        """
        if 'rename' in config:
            rename_dict = config['rename']
            rename_vars = list(rename_dict.keys())

        for var in namespace['raw'].values():
            if 'drop' in config and cls.match(config['drop'], var.name):
                print('Dropping branch: {}'.format(var.name))
                continue

            if 'rename' in config and cls.match(rename_vars, var.name):
                renamed_var = rename_dict[var.name]
                namespace['rename'][renamed_var] = BabyVariable(
                    renamed_var, var.type, [var.name])
                continue

            if 'keep' in config and cls.match(config['keep'], var.name):
                namespace['keep'][var.name] = BabyVariable(
                    var.name, var.type, [var.name])

    @staticmethod
    def parse_calculation(config, namespace):
        """
        Parse ``calculation`` section.
        """
        if 'calculation' in config:
            for name, code in config['calculation'].items():
                try:
                    datatype, *rvalues = [i.strip() for i in code.split(';')]
                except Exception:
                    raise ValueError('Illegal specification for {}: {}.'.format(
                        name, code
                    ))

                output = True
                if '^' in datatype:
                    datatype = datatype.strip('^')
                    output = False

                namespace['calculation'][name] = BabyVariable(
                    name, datatype, rvalues, output=output)

    @classmethod
    def parse_selection(cls, config, namespace):
        """
        Parse ``selection`` section.
        """
        if 'selection' in config:
            for idx, expr in enumerate(config['selection']):
                namespace['selection']['sel'+str(idx)] = BabyVariable(
                    'sel'+str(idx), rvalues=[expr],
                    input=False, output=False, fake=True)

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
