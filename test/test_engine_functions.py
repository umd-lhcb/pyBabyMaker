#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Fri Sep 04, 2020 at 03:31 AM +0800

from pyBabyMaker.engine.functions import macro_funcs


def test_func_identity():
    assert macro_funcs['identity'](1) == 1


def test_func_join():
    assert macro_funcs['join'](['1', '2'], ', ') == '1, 2'


def test_func_format():
    assert macro_funcs['format']('{}-{}-{}', 1, 2, 3) == '1-2-3'


def test_func_deref_var():
    expr = 'a > b_1 && b_1 < c'
    vars_to_deref = ['a', 'b_1', 'c']
    assert macro_funcs['deref_var'](expr, vars_to_deref) == \
        '(*a) > (*b_1) && (*b_1) < (*c)'


def test_func_format_list():
    lst = ['cmath', 'std']
    assert macro_funcs['format_list']('#include <{}>', lst) == \
        ['#include <cmath>', '#include <std>']
