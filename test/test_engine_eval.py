#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Mon Aug 31, 2020 at 04:57 PM +0800

from pyBabyMaker.engine.eval import DelayedEvaluator
from pyBabyMaker.engine.eval import TransForTemplateMacro
from pyBabyMaker.engine.syntax import template_macro_parser


def test_DelayedEvaluator_simple():
    exe = DelayedEvaluator('join', (['a', 'b'], '.'))
    assert exe.eval() == 'a.b'


def test_DelayedEvaluator_nested():
    inner = DelayedEvaluator('join', (['a', 'b'], '.'))
    outer = DelayedEvaluator('identity', (inner, ))
    assert outer.eval() == 'a.b'


def test_TransForTemplateMacro_int():
    expr = template_macro_parser.parse('1')
    transformer = TransForTemplateMacro([], {})
    assert transformer.transform(expr) == 1


def test_TransForTemplateMacro_float():
    expr = template_macro_parser.parse('1.2')
    transformer = TransForTemplateMacro([], {})
    assert transformer.transform(expr) == 1.2


def test_TransForTemplateMacro_boolean():
    expr = template_macro_parser.parse('false')
    transformer = TransForTemplateMacro([], {})
    assert not transformer.transform(expr)


def test_TransForTemplateMacro_str():
    expr = template_macro_parser.parse('"random_str"')
    transformer = TransForTemplateMacro([], {})
    assert transformer.transform(expr) == 'random_str'


def test_TransForTemplateMacro_neg():
    expr = template_macro_parser.parse('-some_var')
    transformer = TransForTemplateMacro([], {'some_var': 1})
    assert transformer.transform(expr) == -1
