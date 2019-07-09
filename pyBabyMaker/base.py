#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Tue Jul 09, 2019 at 05:34 AM -0400

import abc
import yaml
import re
import os
import subprocess

from datetime import datetime
from shutil import which
from .io.TupleDump import PyTupleDump


#########################
# Configuration helpers #
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


###############################
# C++ code generator template #
###############################

class CppGenerator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def parse_conf(self, yaml_conf):
        '''
        Parse configuration file for the writer.
        '''

    @abc.abstractmethod
    def write(self, cpp_file):
        '''
        Write generated C++ file to 'cpp_file'.
        '''

    @staticmethod
    def read_yaml(yaml_file):
        '''
        Read ntuple data structure.
        '''
        with open(yaml_file) as f:
            return yaml.load(f, NestedYAMLLoader)

    @staticmethod
    def dump_ntuple(data_filename):
        dumper = PyTupleDump(data_filename)
        return dumper.dump()

    @staticmethod
    def match(patterns, string, return_value=True):
        for p in patterns:
            if bool(re.search(p, string)):
                return return_value
        return not return_value

    @staticmethod
    def reformat(filename, formatter='clang-format', exec='clang-format -i'):
        if which(formatter):
            cmd_splitted = exec.split(' ')
            cmd_splitted.append(filename)
            subprocess.Popen(cmd_splitted)

    ################
    # C++ Snippets #
    ################

    @staticmethod
    def cpp_gen_date(time_format='%Y-%m-%d %H:%M:%S.%f'):
        return '// Generated on: {}\n'.format(
            datetime.now().strftime(time_format))

    @staticmethod
    def cpp_header(header):
        return '#include <{}>'.format(header)

    @staticmethod
    def cpp_make_var(name, prefix='', suffix='', separator='_'):
        return prefix + separator + re.sub('/', separator, name) + separator + \
            suffix

    @staticmethod
    def cpp_main(definitions, main):
        return '''
{0}

int main(int, char** argv) {{
  {1}
  return 0;
}}
    '''.format(definitions, main)

    @staticmethod
    def cpp_TTree(var, name):
        return 'TTree {0}("{1}", "{1}");\n'.format(var, name)

    @staticmethod
    def cpp_TTreeReader(var, name, TFile):
        return 'TTreeReader {0}("{1}", {2});\n'.format(var, name, TFile)

    @staticmethod
    def cpp_TTreeReaderValue(datatype, var, TTree, TBranch):
        return 'TTreeReaderValue<{0}> {1}({2}, "{3}");\n'
