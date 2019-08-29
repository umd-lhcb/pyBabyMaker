#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Wed Aug 28, 2019 at 11:26 PM -0400

import abc
import yaml
import re
import os
import subprocess

from datetime import datetime
from shutil import which


#########################
# Configuration-related #
#########################

class NestedYAMLLoader(yaml.SafeLoader):
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super().__init__(stream)

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))

        with open(filename, 'r') as f:
            return yaml.load(f, NestedYAMLLoader)


NestedYAMLLoader.add_constructor('!include', NestedYAMLLoader.include)


class ConfigParser(object):
    @staticmethod
    def match(patterns, string, return_value=True):
        for p in patterns:
            if bool(re.search(p, string)):
                return return_value
        return not return_value


###############################
# C++ code generator template #
###############################

class CppGenerator(metaclass=abc.ABCMeta):
    cpp_input_filename = 'input_file'
    cpp_output_filename = 'output_file'

    def __init__(self,
                 io_directive=None, calc_directive=None,
                 additional_system_headers=None, additional_user_headers=None):
        self.io_directive = io_directive
        self.calc_directive = calc_directive

        self.system_headers = ['TFile.h', 'TTree.h', 'TTreeReader.h',
                               'TBranch.h']
        self.user_headers = []

        if additional_system_headers is not None:
            self.system_headers += additional_system_headers

        if additional_user_headers is not None:
            self.user_headers += additional_user_headers

    def gen_headers(self):
        system_headers = ''.join([
            self.cpp_header(i) for i in self.system_headers])
        user_headers = ''.join([
            self.cpp_header(i, system=False) for i in self.user_headers])
        return system_headers + '\n' + user_headers

    ################
    # C++ Snippets #
    ################

    @staticmethod
    def cpp_gen_date(time_format='%Y-%m-%d %H:%M:%S.%f'):
        return '// Generated on: {}\n'.format(
            datetime.now().strftime(time_format))

    @staticmethod
    def cpp_header(header, system=True):
        if system:
            return '#include <{}>\n'.format(header)
        else:
            return '#include "{}"\n'.format(header)

    @staticmethod
    def cpp_make_var(name, prefix='', suffix='', separator='_'):
        return prefix + separator + re.sub('/', separator, name) + separator + \
            suffix

    @staticmethod
    def cpp_main(body):
        return '''
int main(int, char** argv) {{
  {0}
  return 0;
}}
    '''.format(body)

    @staticmethod
    def cpp_TTree(var, name):
        return 'TTree {0}("{1}", "{1}");\n'.format(var, name)

    @staticmethod
    def cpp_TTreeReader(var, name, TFile):
        return 'TTreeReader {0}("{1}", {2});\n'.format(var, name, TFile)

    @staticmethod
    def cpp_TTreeReaderValue(datatype, var, TTree, TBranch):
        return 'TTreeReaderValue<{0}> {1}({2}, "{3}");\n'


##################
# Skeleton maker #
##################

class SkeletonMaker(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def parse_conf(self, filename):
        '''
        Parse configuration file for the writer.
        '''

    @abc.abstractmethod
    def write(self, filename):
        '''
        Write generated C++ file.
        '''

    @staticmethod
    def read(yaml_filename):
        '''
        Read ntuple data structure.
        '''
        with open(yaml_filename) as f:
            return yaml.load(f, NestedYAMLLoader)

    @staticmethod
    def reformat(cpp_filename, formatter='clang-format', exec='clang-format -i'):
        if which(formatter):
            cmd_splitted = exec.split(' ')
            cmd_splitted.append(cpp_filename)
            subprocess.Popen(cmd_splitted)

    @staticmethod
    def dump(data_filename):
        from pyBabyMaker.io.TupleDump import PyTupleDump
        dumper = PyTupleDump(data_filename)
        return dumper.dump()
