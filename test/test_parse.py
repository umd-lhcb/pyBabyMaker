#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Tue Sep 03, 2019 at 05:46 PM -0400

from pyBabyMaker.parse import is_numeral, find_all_args


def test_is_numeral_int():
    assert is_numeral(1)


def test_is_numeral_float():
    assert is_numeral(3.14)


def test_is_numeral_str():
    assert is_numeral('3.14')


def test_is_numeral_variable():
    assert not is_numeral('Var3')


def test_find_all_args_simple():
    assert find_all_args('FUNC1(arg1, arg2)') == ['arg1', 'arg2']
