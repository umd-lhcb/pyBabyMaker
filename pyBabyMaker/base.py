#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Sat Jul 06, 2019 at 09:49 PM -0400

import abc
import yaml
import re
import subprocess

from datetime import datetime
from shutil import which
from .io.TupleDump import PyTupleDump


###############################
# C++ code generator template #
###############################

class CppGenerator(metaclass=abc.ABCMeta):
    def __init__(self, data_filename):
        dumper = PyTupleDump(data_filename)
        self.raw_datatype = dumper.dump()

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
            return yaml.safe_load(f)

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

    @staticmethod
    def cpp_gen_date(time_format='%Y-%m-%d %H:%M:%S.%f'):
        return '// Generated on: {}\n'.format(
            datetime.now().strftime(time_format))

    @staticmethod
    def cpp_header(header):
        return '#include <{}>'.format(header)

    @staticmethod
    def cpp_main(definitions, main):
        return '''
{0}

int main(int, char** argv) {{
  {1}
  return 0;
}}
    '''.format(definitions, main)
