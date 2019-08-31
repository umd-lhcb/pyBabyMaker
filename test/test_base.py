#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Fri Aug 30, 2019 at 08:15 PM -0400

import unittest

from pyBabyMaker.base import UniqueList
from pyBabyMaker.base import BaseCppGenerator


##################
# Data structure #
##################

def test_UniqueList__init__():
    test_list = UniqueList([1, 2, 3, 4])
    assert test_list == [1, 2, 3, 4]


class UniqueListTester(unittest.TestCase):
    def test___init__(self):
        self.assertTrue(
            [1, 2, 3, 4],
            UniqueList([1, 2, 3, 4]),
        )
        self.assertTrue(
            [1, 2, 3],
            UniqueList([1, 2, 3, 1]),
        )


#######################
# C++ code generators #
#######################

class SimpleCppGenerator(BaseCppGenerator):
    def gen_preamble(self):
        pass

    def gen_body(self):
        pass


class SimpleCppGeneratorTester(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cpp_generator = SimpleCppGenerator(
            additional_system_headers=['iostream'],
            additional_user_headers=['include/dummy.h']
        )

    #####################
    # Initializer tests #
    #####################

    def test_system_headers(self):
        self.assertEqual(
            ['TFile.h', 'TTree.h', 'TTreeReader.h', 'TBranch.h', 'iostream'],
            self.cpp_generator.system_headers
        )

    def test_user_headers(self):
        self.assertEqual(
            ['include/dummy.h'],
            self.cpp_generator.user_headers
        )

    ###############################
    # Chunk code generation tests #
    ###############################

    def test_gen_headers(self):
        self.assertEqual(
            '''#include <TFile.h>
#include <TTree.h>
#include <TTreeReader.h>
#include <TBranch.h>
#include <iostream>

#include "include/dummy.h"
''',
            self.cpp_generator.gen_headers()
        )

    def test_gen_headers_no_user(self):
        cpp_generator = SimpleCppGenerator()
        self.assertEqual(
            '''#include <TFile.h>
#include <TTree.h>
#include <TTreeReader.h>
#include <TBranch.h>

''',
            cpp_generator.gen_headers()
        )

    ######################
    # C++ snippets tests #
    ######################

    def test_cpp_header_system(self):
        self.assertEqual(
            '#include <iostream>\n',
            self.cpp_generator.cpp_header('iostream')
        )

    def test_cpp_header_user(self):
        self.assertEqual(
            '#include "include/dummy.h"\n',
            self.cpp_generator.cpp_header('include/dummy.h', False)
        )

    def test_cpp_make_var(self):
        self.assertEqual(
            'pre_Variable1_Old_suf',
            self.cpp_generator.cpp_make_var(
                'Variable1/Old',
                prefix='pre', suffix='suf', separator='_'
            )
        )

    def test_cpp_main(self):
        self.assertEqual(
            '''
int main(int, char** argv) {
  body
  return 0;
}''',
            self.cpp_generator.cpp_main('body')
        )

    def test_cpp_TTree(self):
        self.assertEqual(
            'TTree tree("tree", "tree");\n',
            self.cpp_generator.cpp_TTree('tree', 'tree')
        )

    def test_cpp_TTreeReader(self):
        self.assertEqual(
            'TTreeReader reader("tree", input_file);\n',
            self.cpp_generator.cpp_TTreeReader('reader', 'tree', 'input_file')
        )

    def test_cpp_TTreeReaderValue(self):
        self.assertEqual(
            'TTreeReaderValue<float> value(reader, "some_branch");\n',
            self.cpp_generator.cpp_TTreeReaderValue(
                'float', 'value', 'reader', 'some_branch')
        )


if __name__ == '__main__':
    unittest.main()
