#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Sat Sep 05, 2020 at 02:53 AM +0800

import re

from pyBabyMaker.base import UniqueList, BaseMaker, Variable
from pyBabyMaker.boolean.utils import find_all_vars
from pyBabyMaker.engine.core import template_transformer, template_evaluator


########################
# Configuration parser #
########################

class BabyConfigParser(object):
    """
    Basic parser for YAML C++ code instruction.
    """
    def __init__(self, parsed_config, dumped_ntuple):
        """
        Initialize the config parser with parsed YAML file and dumped n-tuple
        structure.
        """
        self.parsed_config = parsed_config
        self.dumped_ntuple = dumped_ntuple

    def parse(self):
        """
        Parse the loaded YAML dict (in ``self.parsed_config`) and dumped ntuple
        tree structure (in ``self.dumped_ntuple``).
        """
        directive = {
            'system_headers': UniqueList(),
            'user_headers': UniqueList(),
            'trees': {},
        }

        for output_tree, config in self.parsed_config.items():
            input_tree = config['input_tree']
            dumped_tree = self.dumped_ntuple[input_tree]

            subdirective = self.gen_subdirective(input_tree)

            self.parse_headers(config, directive)
            self.parse_drop_keep_rename(config, dumped_tree, subdirective)
            self.parse_calculation(config, dumped_tree, subdirective)
            self.parse_selection(config, dumped_tree, subdirective)

            subdirective['input_branch_names'] = [
                v.name for v in subdirective['input_branches']]

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
                directive['known_names'].append(br_in)

        for datatype, br_in in branches_to_keep:
            directive['input_branches'].append(Variable(datatype, br_in))
            try:
                # Handle possible branch rename here
                br_out = config['rename'][br_in]
            except KeyError:
                br_out = br_in

            directive['output_branches'].append(
                Variable(datatype, br_out, br_in))

    def parse_calculation(self, config, dumped_tree, directive):
        """
        Parse ``calculation`` section.
        """
        if 'calculation' in config:
            for name, code in config['calculation'].items():
                datatype, rvalue = code.split(';')
                directive['known_names'].append(name)

                if '^' in datatype:
                    datatype = datatype.strip('^')
                    directive['temp_variables'].append(
                        Variable(datatype, name, rvalue))
                    self.load_missing_vars(rvalue, dumped_tree, directive)

                else:
                    directive['output_branches'].append(
                        Variable(datatype, name, rvalue))
                    self.load_missing_vars(rvalue, dumped_tree, directive)

    def parse_selection(self, config, dumped_tree, directive):
        """
        Parse ``selection`` section.
        """
        if 'selection' in config:
            directive['selection'] = config['selection']

            for expr in config['selection']:
                self.load_missing_vars(expr, dumped_tree, directive)

    def load_missing_vars(self, expr, dumped_tree, directive):
        """
        Load missing variables required for calculation or comparison, provided
        that the variables are available directly in the ntuple.
        """
        variables = UniqueList(find_all_vars(expr))

        for v in variables:
            if v not in directive['known_names']:
                try:
                    datatype = self.load_var(v, dumped_tree)
                    directive['input_branches'].append(
                        Variable(datatype, v))
                    directive['known_names'].append(v)
                except Exception:
                    print('WARNING: {} is not a known branch name.'.format(v))

    @staticmethod
    def gen_subdirective(input_tree):
        return {'input_tree': input_tree,
                'input_branches': UniqueList(),
                'output_branches': UniqueList(),
                'temp_variables': UniqueList(),
                'selection': ['true'],
                'known_names': UniqueList(),
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
        Initialize with path to YAML file and n-tuple file.
        """
        self.config_filename = config_filename
        self.ntuple_filename = ntuple_filename
        self.template_filename = template_filename
        self.use_reformater = use_reformater

    def gen(self, filename, **kwargs):
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
