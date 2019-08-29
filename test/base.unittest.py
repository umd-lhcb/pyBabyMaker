#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Wed Aug 28, 2019 at 11:27 PM -0400

import sys
sys.path.insert(0, '..')

import unittest

from pyBabyMaker.base import CppGenerator


class BaseCppGenerator(CppGenerator):
    pass


class CppGeneratorTester(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cpp_generator = BaseCppGenerator(
            additional_system_headers=['iostream'],
            additional_user_headers=['include/dummy.h']
        )

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
        local_cpp_generator = BaseCppGenerator()
        self.assertEqual(
            '''#include <TFile.h>
#include <TTree.h>
#include <TTreeReader.h>
#include <TBranch.h>

''',
            local_cpp_generator.gen_headers()
        )


if __name__ == '__main__':
    unittest.main()
