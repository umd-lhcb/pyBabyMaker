#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Mon Sep 09, 2019 at 12:09 AM -0400
"""
This module provides basic infrastructure for n-tuple related C++ code
generation.
"""

import abc
import yaml
import re
import subprocess

from collections import namedtuple
from datetime import datetime
from shutil import which

from pyBabyMaker.parse import find_all_vars


##################
# Data structure #
##################

class UniqueList(list):
    """
    An extension to the standard ``list`` class such that every element stored
    inside is unique.
    """
    def __init__(self, iterable=None):
        """
        This initializer takes an optional iterable and store the unique
        elements inside that iterable only.
        """
        try:
            uniq = []
            [uniq.append(i) for i in iterable if not uniq.count(i)]
            super().__init__(uniq)
        except TypeError:
            super().__init__()

    def append(self, object):
        if not super().__contains__(object):
            super().append(object)

    def insert(self, index, object):
        if not super().__contains__(object):
            super().insert(index, object)

    def __add__(self, value):
        return UniqueList(super().__add__(value))

    def __iadd__(self, value):
        return UniqueList(super().__iadd__(value))


Variable = namedtuple('Variable', 'type name rvalue, dependency',
                      defaults=(None, None))


class CppCodeDataStore(object):
    """
    Store the data structure for C++ code to be generated.
    """
    def __init__(self, input_file=None, output_file=None,
                 input_tree=None, output_tree=None, selection=None,
                 input_br=None, output_br=None, transient=None):
        """
        Initialize code data store.
        """
        self.input_file = input_file
        self.output_file = output_file
        self.input_tree = input_tree
        self.output_tree = output_tree
        self.selection = selection

        self.input_br = UniqueList(input_br)
        self.output_br = UniqueList(output_br)
        self.transient = UniqueList(transient)

        # Record all loaded variables
        self.loaded_variables = UniqueList()

    def append(self, variable, target):
        """
        Append ``variable`` to ``target``, with the constraint that ``variable``
        must be of ``Variable`` type.
        """
        if type(variable) is not Variable:
            raise TypeError('Type {} is not a valid Variable!'.format(
                type(variable)
            ))
        else:
            self.__getattribute__(target).append(variable)

    def append_input_br(self, variable):
        """
        Append ``variable`` to ``self.input_br``, validating that ``variable``
        has the correct type.

        This will also mark ``variable.name`` as loaded.
        """
        self.append(variable, 'input_br')
        self.loaded_variables.append(variable.name)

    def append_output_br(self, variable):
        """
        Append ``variable`` to ``self.output_br``, validating that ``variable``
        has the correct type.
        """
        self.append(variable, 'output_br')

    def append_transient(self, variable):
        """
        Append ``variable`` to ``self.transient``, validating that ``variable``
        has the correct type.

        This will also mark ``variable.name`` as loaded.
        """
        self.append(variable, 'transient')
        self.loaded_variables.append(variable.name)


###########
# Parsers #
###########

class BaseConfigParser(object):
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

        self.system_headers = UniqueList()
        self.user_headers = UniqueList()
        self.instructions = []

    def parse(self):
        """
        Parse the loaded YAML dict (in ``self.parsed_config`) and dumped n-tuple
        tree structure (in ``self.dumped_ntuple``).
        """
        for output_tree, config in self.parsed_config.items():
            input_tree = config['input_tree']
            dumped_tree = self.dumped_ntuple[input_tree]
            data_store = CppCodeDataStore(input_tree=input_tree,
                                          output_tree=output_tree)

            self.parse_headers(config)
            self.parse_drop_keep_rename(config, dumped_tree, data_store)
            self.parse_calculation(config, dumped_tree, data_store)
            self.parse_selection(config, dumped_tree, data_store)

            self.instructions.append(data_store)

    def parse_headers(self, config):
        """
        Parse ``headers`` section.
        """
        try:
            self.system_headers += config['headers']['system']
        except KeyError:
            pass

        try:
            self.user_headers += config['headers']['user']
        except KeyError:
            pass

    def parse_drop_keep_rename(self, config, dumped_tree, data_store):
        """
        Parse ``drop, keep, rename`` sections.
        """
        branches_to_keep = []
        for br_in, datatype in dumped_tree.items():
            if 'drop' in config.keys() and self.match(config['drop'], br_in):
                print('Dropping branch: {}'.format(br_in))
            elif 'keep' in config.keys() and self.match(config['keep'], br_in):
                branches_to_keep.append((datatype, br_in))
            elif 'rename' in config.keys() and br_in in config['rename']:
                branches_to_keep.append((datatype, br_in))

        for datatype, br_in in branches_to_keep:
            data_store.append_input_br(Variable(datatype, br_in))
            # Handle branch rename here
            try:
                br_out = config['rename'][br_in]
                data_store.append_output_br(Variable(datatype, br_out, br_in))
            except KeyError:
                data_store.append_output_br(Variable(datatype, br_in, br_in))

    def parse_calculation(self, config, dumped_tree, data_store):
        """
        Parse ``calculation`` section.
        """
        if 'calculation' in config.keys():
            for name, code in config['calculation'].items():
                datatype, rvalue = code.split(';')
                if datatype == '^':
                    self.__getattribute__(rvalue)(name, dumped_tree, data_store)
                elif '^' in datatype:
                    datatype = datatype.strip('^')
                    data_store.append_transient(
                        Variable(datatype, name, rvalue)
                    )
                    self.load_missing_variables(rvalue, dumped_tree, data_store)
                else:
                    data_store.append_output_br(
                        Variable(datatype, name, rvalue)
                    )
                    self.load_missing_variables(rvalue, dumped_tree, data_store)

    def parse_selection(self, config, dumped_tree, data_store):
        """
        Parse ``selection`` section.
        """
        if 'selection' in config.keys():
            data_store.selection = ' '.join(config['selection'])
            self.load_missing_variables(data_store.selection, dumped_tree,
                                        data_store)

    def load_missing_variables(self, expr, dumped_tree, data_store):
        """
        Load missing variables required for calculation or comparison, provided
        that the variables are available directly in the n-tuple.
        """
        variables = find_all_vars(expr)
        for v in variables:
            if v not in data_store.loaded_variables:
                self.LOAD(v, dumped_tree, data_store)

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
    def LOAD(name, dumped_tree, data_store):
        """
        Load variable ``name`` from n-tuple, if it's available.
        """
        try:
            datatype = dumped_tree[name]
            data_store.append_input_br(
                Variable(datatype, name))
        except KeyError:
            raise KeyError('Branch {} not found.'.format(name))


#######################
# C++ code generators #
#######################


class BaseCppGenerator(metaclass=abc.ABCMeta):
    """
    Basic C++ code snippets for n-tuple processing.
    """
    def __init__(self, instructions,
                 additional_system_headers=None, additional_user_headers=None,
                 add_timestamp=True):
        self.instructions = instructions
        self.add_timestamp = add_timestamp
        self.system_headers = ['TFile.h', 'TTree.h', 'TTreeReader.h',
                               'TBranch.h']
        self.user_headers = []

        if additional_system_headers is not None:
            self.system_headers += additional_system_headers

        if additional_user_headers is not None:
            self.user_headers += additional_user_headers

    # Code generation ##########################################################

    def gen_timestamp(self):
        """
        Generate a timestamp.
        """
        if self.add_timestamp:
            return self.cpp_gen_date()
        else:
            return ''

    def gen_headers(self):
        """
        Generate C++ ``#include`` macros.
        """
        system_headers = ''.join([
            self.cpp_header(i) for i in self.system_headers])
        user_headers = ''.join([
            self.cpp_header(i, system=False) for i in self.user_headers])
        return system_headers + '\n' + user_headers

    @abc.abstractmethod
    def gen(self):
        """
        Generate the full C++ output code.
        """

    @abc.abstractmethod
    def gen_preamble(self):
        """
        Generate C++ definitions and functions before ``main``.
        """

    @abc.abstractmethod
    def gen_body(self):
        '''
        Generate C++ code inside ``main`` function.
        '''

    # Helpers ##################################################################

    @staticmethod
    def dereference_variables(expr, vars_to_deref):
        """
        Dereference variables loaded from n-tuple directly. For example:

        .. code-block:: c++

            TTreeReader reader("tree", input_file)
            TTreeReaderValue<double> Y_PT(reader, "Y_PT");

            while (reader.Next()) {
                cout << (*Y_PT)
            }

        The ``Y_PT`` inside the ``while`` loop needs to be dereferenced.
        """
        variables = UniqueList(find_all_vars(expr))
        ref_variables = [v.name for v in vars_to_deref]

        for v in variables:
            if v in ref_variables:
                expr = re.sub(v, '(*{})'.format(v), expr)

        return expr

    # C++ snippets #############################################################

    @staticmethod
    def cpp_gen_date(time_format='%Y-%m-%d %H:%M:%S.%f'):
        """
        C++ code generation time stamp.
        """
        return '// Generated on: {}\n'.format(
            datetime.now().strftime(time_format))

    @staticmethod
    def cpp_header(header, system=True):
        """
        C++ ``#include`` snippets.
        """
        if system:
            return '#include <{}>\n'.format(header)
        else:
            return '#include "{}"\n'.format(header)

    @staticmethod
    def cpp_make_var(name, prefix='', suffix='', separator='_'):
        """
        Make a legal C++ variable name. This is typically used to convert a
        ``TTree`` name to a C++ variable name.
        """
        if prefix != '':
            prefix += separator
        if suffix != '':
            suffix = separator + suffix
        return prefix + re.sub('/', separator, name) + suffix

    @staticmethod
    def cpp_main(body):
        """
        C++ (dumb) main function snippet.
        """
        return '''
int main(int, char** argv) {{
  {0}
  return 0;
}}'''.format(body)

    @staticmethod
    def cpp_TTree(var, name):
        """
        C++ ``TTree`` initializer snippet.
        """
        return 'TTree {0}("{1}", "{1}");\n'.format(var, name)

    @staticmethod
    def cpp_TTreeReader(var, name, TFile):
        """
        C++ ``TTreeReader`` initializer snippet.
        """
        return 'TTreeReader {0}("{1}", {2});\n'.format(var, name, TFile)

    @staticmethod
    def cpp_TTreeReaderValue(datatype, var, TTreeReader, branch_name):
        """
        C++ ``TTreeReaderValue`` initializer snippet.
        """
        return 'TTreeReaderValue<{0}> {1}({2}, "{3}");\n'.format(
            datatype, var, TTreeReader, branch_name
        )


##############
# Base maker #
##############

class BaseMaker(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def parse_config(self, config_filename):
        """
        Parse configuration file for the writer.
        """

    @abc.abstractmethod
    def gen(self, filename):
        """
        Generate C++ code and write it to file.
        """

    @staticmethod
    def read(yaml_filename):
        """
        Read C++ code generation instruction stored in a YAML.
        """
        from pyBabyMaker.io.NestedYAMLLoader import NestedYAMLLoader
        with open(yaml_filename) as f:
            return yaml.load(f, NestedYAMLLoader)

    @staticmethod
    def dump(data_filename):
        """
        Dump ``TTree`` structures inside a n-tuple
        """
        from pyBabyMaker.io.TupleDump import PyTupleDump
        dumper = PyTupleDump(data_filename)
        return dumper.dump()

    @staticmethod
    def reformat(cpp_filename, formatter='clang-format', flags=['-i']):
        """
        Optionally reformat C++ code after generation, if the ``formatter`` is
        in ``$PATH``.
        """
        if which(formatter):
            cmd = [formatter] + flags + [cpp_filename]
            subprocess.Popen(cmd)
