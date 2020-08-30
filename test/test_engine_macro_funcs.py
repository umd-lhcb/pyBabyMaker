#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Mon Aug 31, 2020 at 04:08 AM +0800

from pyBabyMaker.engine.macro_funcs import macro_funcs


def test_func_join():
    assert macro_funcs['join'](['1', '2'], ', ') == '1, 2'
