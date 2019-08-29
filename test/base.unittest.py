#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Wed Aug 28, 2019 at 10:52 PM -0400

import sys
sys.path.insert(0, '..')

import unittest

from pyBabyMaker.base import CppGenerator


class CppGeneratorTester(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cpp_generator = CppGenerator(additional_headers=['cmath'])

    def test_headers(self):
        self.assertEqual(
            self.cpp_generator.headers,
            ['TFile.h', 'TTree.h', 'TTreeReader.h', 'TBranch.h', 'cmath']
        )


if __name__ == '__main__':
    unittest.main()
