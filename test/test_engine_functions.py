#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Mon Aug 31, 2020 at 04:46 AM +0800

from pyBabyMaker.engine.functions import macro_funcs


def test_func_identity():
    assert macro_funcs['identity'](1) == 1


def test_func_join():
    assert macro_funcs['join'](['1', '2'], ', ') == '1, 2'
