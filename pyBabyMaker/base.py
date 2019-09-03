#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Tue Sep 03, 2019 at 12:06 PM -0400
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

IO = namedtuple('IO', 'input output')


class CppCodeDataStore(object):
    """
    Store the data structure for C++ code to be generated.
    """
    def __init__(self, input_file=None, output_file=None,
                 input_tree=None, output_tree=None,
                 input_br=None, output_br=None, transient=None):
        """
        Initialize code data store.
        """
        self.input_file = input_file
        self.output_file = output_file
        self.input_tree = input_tree
        self.output_tree = output_tree

        self.input_br = UniqueList(input_br)
        self.output_br = UniqueList(output_br)
        self.transient = UniqueList(transient)

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
        self.append(variable, 'input_br')

    def append_output_br(self, variable):
        self.append(variable, 'output_br')

    def append_transient(self, variable):
        self.append(variable, 'transient')


###########
# Parsers #
###########

class BaseConfigParser(object):
    """
    Basic parser for YAML C++ code instruction.
    """
    def __init__(self, parsed_config, dumped_ntp):
        """
        Initialize the config parser with parsed YAML file and dumped n-tuple
        structure.
        """
        self.parse_config = parsed_config
        self.parsed_ntp = dumped_ntp

        self.system_headers = UniqueList()
        self.user_headers = UniqueList()
        self.instructions = dict()

    def parse_headers(self, config_section):
        try:
            self.system_headers += config_section['headers']['system']
        except KeyError:
            pass

        try:
            self.user_headers += config_section['headers']['user']
        except KeyError:
            pass

    def parse_drop_keep_rename(self, config_section, dumped_tree, data_store):
        for br_in, datatype in dumped_tree.items():
            if 'drop' in config_section.keys() and self.match(
                    config_section['drop'], br_in):
                print('Dropping branch: {}'.format(br_in))

            elif self.match(config_section['keep'], br_in):
                data_store.append_input_br(Variable(datatype, br_in, None))
                data_store.append_output_br(Variable(datatype, br_in, None))

            elif 'rename' in config_section.keys():
                try:
                    br_out = config_section['rename'][br_in]
                    data_store.append_input_br(Variable(datatype, br_in, None))
                    data_store.append_output_br(Variable(datatype, br_out,
                                                         None))
                except KeyError:
                    pass

    @staticmethod
    def match(patterns, string, return_value=True):
        """
        Test if ``string`` (a regular expression) matches at least one element
        in the ``patterns``. If there's a match, return ``return_value``.
        """
        for p in patterns:
            if bool(re.search(p, string)):
                return return_value
        return not return_value


#######################
# C++ code generators #
#######################


class BaseCppGenerator(metaclass=abc.ABCMeta):
    """
    Basic C++ code snippets for n-tuple processing.
    """
    cpp_input_filename = 'input_file'
    cpp_output_filename = 'output_file'

    def __init__(self, instructions,
                 additional_system_headers=None, additional_user_headers=None):
        self.instructions = instructions
        self.preamble = []
        self.main = []

        self.system_headers = ['TFile.h', 'TTree.h', 'TTreeReader.h',
                               'TBranch.h']
        self.user_headers = []

        if additional_system_headers is not None:
            self.system_headers += additional_system_headers

        if additional_user_headers is not None:
            self.user_headers += additional_user_headers

    ###################
    # Code generation #
    ###################

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
    def gen_preamble(self):
        """
        Generate C++ definitions and functions before ``main``.
        """

    @abc.abstractmethod
    def gen_body(self):
        '''
        Generate C++ code inside ``main`` function.
        '''

    ################
    # C++ snippets #
    ################

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
        return prefix + separator + re.sub('/', separator, name) + separator + \
            suffix

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
    def parse_conf(self, filename):
        """
        Parse configuration file for the writer.
        """

    @abc.abstractmethod
    def write(self, filename):
        """
        Write generated C++ file.
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
