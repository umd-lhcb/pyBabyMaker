#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Fri Jan 08, 2021 at 04:00 AM +0100

from pyBabyMaker.var_resolver import Variable


##############
# Containers #
##############

def test_Variable_simple():
    var = Variable('test')

    assert var.name == 'test'
    assert var.type == 'nil'
    assert var.deps == {}
    assert var.resolved == {}
    assert var.idx == 0
