#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Mon Aug 31, 2020 at 08:44 PM +0800

from pyBabyMaker.engine.functions import macro_funcs


def test_func_identity():
    assert macro_funcs['identity'](1) == 1


def test_func_join():
    assert macro_funcs['join'](['1', '2'], ', ') == '1, 2'


def test_func_format():
    assert macro_funcs['format']('{}-{}-{}', 1, 2, 3) == '1-2-3'
