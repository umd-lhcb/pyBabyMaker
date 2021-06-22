#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Tue Jun 22, 2021 at 02:46 AM +0200

from pyBabyMaker.boolean.utils import find_all_args, find_all_vars


def test_find_all_args_simple():
    assert find_all_args('FUNC1(arg1, arg2)') == ['arg1', 'arg2']


def test_find_all_args_nested():
    assert find_all_args(
        'FUNC1(arg1, arg2, Rand(arg3, arg4, FUNC2(arg5 * 2.3, arg6 + arg7)))'
    ) == ['arg5', 'arg6', 'arg7', 'arg3', 'arg4', 'arg1', 'arg2']


def test_find_all_args_bool():
    assert find_all_args(
        '!(FUNC1(arg1, arg2) > 1 && FUNC2(FUNC3(arg3, arg4, FUNC4(1, 2)) +'
        'arg6)) <= 3 || FUNC6(arg7 != 3, arg8, arg9*FUNC7())'
    ) == ['arg3', 'arg4', 'arg1', 'arg2', 'arg6', 'arg7', 'arg9', 'arg8']


def test_find_all_vars():
    assert find_all_vars(
        '!(FUNC1(arg1, arg2) && FUNC2(FUNC3(arg3, arg4, FUNC4(1, 2)) + arg6))||'
        'FUNC6(arg7, arg8, arg9*FUNC7(arg10+arg11))'
    ) == ['arg3', 'arg4', 'arg10', 'arg11', 'arg6', 'arg1', 'arg2', 'arg9',
          'arg7', 'arg8']


def test_find_all_vars_bracket_init():
    assert find_all_vars(
        '!(FUNC1{arg1, arg2} && FUNC2{FUNC3{arg3, arg4, FUNC4{1, 2}} + arg6})||'
        'FUNC6{arg7, arg8, arg9*FUNC7{arg10+arg11}}'
    ) == ['arg3', 'arg4', 'arg10', 'arg11', 'arg6', 'arg1', 'arg2', 'arg9',
          'arg7', 'arg8']


def test_find_all_vars_with_method_calls():
    assert find_all_vars(
        'arg1->test(arg2, arg3) && arg4->call() && arg5.call(arg6) || arg7.arg8'
    ) == ['arg2', 'arg3', 'arg1', 'arg4', 'arg6', 'arg5', 'arg7']


def test_find_all_vars_with_full_name_func_calls():
    assert find_all_vars('TMath::Sqrt(arg1, arg2)') == ['arg1', 'arg2']
