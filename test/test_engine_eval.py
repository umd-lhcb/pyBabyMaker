#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Mon Aug 31, 2020 at 05:08 AM +0800

from pyBabyMaker.engine.eval import DelayedEvaluator


def test_DelayedEvaluator_simple():
    exe = DelayedEvaluator('join', (['a', 'b'], '.'))
    assert exe.eval() == 'a.b'


def test_DelayedEvaluator_nested():
    inner = DelayedEvaluator('join', (['a', 'b'], '.'))
    outer = DelayedEvaluator('identity', (inner, ))
    assert outer.eval() == 'a.b'
