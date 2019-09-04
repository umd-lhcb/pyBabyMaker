#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Tue Sep 03, 2019 at 11:55 PM -0400

from pyBabyMaker.parse import is_numeral, find_all_args, find_all_vars


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


def test_find_all_args_nested():
    assert find_all_args(
        'FUNC1(arg1, arg2, Rand(arg3, arg4, FUNC2(arg5 * 2.3, arg6 + arg7)))'
    ) == ['arg1', 'arg2', 'arg3', 'arg4', 'arg5', '2.3', 'arg6', 'arg7']


def test_find_all_args_bool():
    assert find_all_args(
        '!(FUNC1(arg1, arg2) > 1 && FUNC2(FUNC3(arg3, arg4, FUNC4(1, 2)) +'
        'arg6)) <= 3 || FUNC6(arg7 != 3, arg8, arg9*FUNC7())'
    ) == ['arg1', 'arg2', '1', 'arg3', 'arg4', '1', '2', 'arg6', '3', 'arg7',
          '3', 'arg8', 'arg9']


def test_find_all_vars():
    assert find_all_vars(
        '!(FUNC1(arg1, arg2) && FUNC2(FUNC3(arg3, arg4, FUNC4(1, 2)) + arg6))||'
        'FUNC6(arg7, arg8, arg9*FUNC7())'
    ) == ['arg1', 'arg2', 'arg3', 'arg4', 'arg6', 'arg7', 'arg8', 'arg9']
