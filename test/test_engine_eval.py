#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Mon Jan 25, 2021 at 05:37 AM +0100

import pytest

from pyBabyMaker.engine.eval import DelayedEvaluator
from pyBabyMaker.engine.eval import ForStmtEvaluator, IfStmtEvaluator
from pyBabyMaker.engine.eval import TransForTemplateMacro, Scope
from pyBabyMaker.engine.syntax import template_macro_parser
from collections import namedtuple


##########################
# Stateless transformers #
##########################

def test_DelayedEvaluator_simple():
    exe = DelayedEvaluator('join', (['a', 'b'], '.'))
    assert exe.eval() == 'a.b'


def test_DelayedEvaluator_nested():
    inner = DelayedEvaluator('join', (['a', 'b'], '.'))
    outer = DelayedEvaluator('identity', (inner, ))
    assert outer.eval() == 'a.b'


def test_DelayedEvaluator_no_arg():
    exe = DelayedEvaluator('one', [])
    assert exe.eval() == 1


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


def test_TransForTemplateMacro_str_escaped_double_quote():
    expr = template_macro_parser.parse('"random_str \\"something\\" "')
    transformer = TransForTemplateMacro([], {})
    assert transformer.transform(expr) == 'random_str "something" '


def test_TransForTemplateMacro_str_unescaped_single_quote():
    expr = template_macro_parser.parse(""" "some 'single quote'" """)
    transformer = TransForTemplateMacro([], {})
    assert transformer.transform(expr) == "some 'single quote'"


def test_TransForTemplateMacro_neg():
    expr = template_macro_parser.parse('-some_var')
    transformer = TransForTemplateMacro([], {'some_var': 1})
    exe = transformer.transform(expr)
    assert exe.eval() == -1


def test_TransForTemplateMacro_func_call():
    expr = template_macro_parser.parse('join: (list: "a", "b"), ","')
    transformer = TransForTemplateMacro([], {})
    exe = transformer.transform(expr)
    assert exe.eval() == 'a,b'


def test_TransForTemplateMacro_getattr_normal():
    container = namedtuple('container', 'value meta')
    expr = template_macro_parser.parse('data.value')
    transformer = TransForTemplateMacro(
        [], {'data': container(1, 2)})
    exe = transformer.transform(expr)
    assert exe.eval() == 1


def test_TransForTemplateMacro_getattr_dict():
    expr = template_macro_parser.parse('data.value')
    transformer = TransForTemplateMacro(
        [], {'data': {'value': 1}})
    exe = transformer.transform(expr)
    assert exe.eval() == 1


def test_TransForTemplateMacro_getattr_complex():
    container = namedtuple('container', 'value meta')
    expr = template_macro_parser.parse('data.value.stuff')
    transformer = TransForTemplateMacro(
        [], {'data': container({'stuff': 1}, 2)})
    exe = transformer.transform(expr)
    assert exe.eval() == 1


def test_TransForTemplateMacro_getitem():
    expr = template_macro_parser.parse('data[1]')
    transformer = TransForTemplateMacro(
        [], {'data': [0, 1]})
    exe = transformer.transform(expr)
    assert exe.eval() == 1


def test_TransForTemplateMacro_method_call():
    class Tester():
        def add(self, x, y):
            return x+y

    expr = template_macro_parser.parse('data.tester->add: 11, 2')
    transformer = TransForTemplateMacro(
        [], {'data': {'tester': Tester()}})
    exe = transformer.transform(expr)
    assert exe.eval() == 13


def test_TransForTemplateMacro_method_call_no_arg():
    expr = template_macro_parser.parse('data.stuff->items:')
    transformer = TransForTemplateMacro(
        [], {'data': {'stuff': {'a': 1, 'b': 2}}})
    exe = transformer.transform(expr)
    assert exe.eval() == {'a': 1, 'b': 2}.items()


def test_TransForTemplateMacro_boolean_call_complex():
    expr = template_macro_parser.parse(
        'a >= b || b < c && d.e >= 1 || d.e <= 1 || c == b')
    transformer = TransForTemplateMacro(
        [], {'a': 3.4, 'b': 2, 'c': 3, 'd': {'e': 1.1}})
    exe = transformer.transform(expr)
    assert exe.eval() is True


#########################
# Stateful transformers #
#########################

@pytest.fixture
def scope():
    return Scope()


def test_TransForTemplateMacro_for_stmt(scope):
    expr = template_macro_parser.parse('for idx in data.value')
    known_symb = {'data': {'value': [1, 2, 3]}}

    transformer = TransForTemplateMacro(scope, known_symb)
    exe = transformer.transform(expr)
    exe.eval()

    assert transformer.scope.parent == scope
    assert transformer.scope.evaluator == exe
    assert known_symb['idx'] == 3


def test_TransForTemplateMacro_for_stmt_nested(scope):
    expr1 = template_macro_parser.parse('for idx in data.value')
    expr2 = template_macro_parser.parse('for j in idx')
    known_symb = {'data': {'value': [[1, 2, 3], [4, 5, 6], [7, 8, 9]]}}

    transformer = TransForTemplateMacro(scope, known_symb)
    exe = transformer.transform(expr1)
    nested_exe = transformer.transform(expr2)
    exe.loop.append(nested_exe)
    exe.eval()

    assert known_symb['idx'] == [7, 8, 9]
    assert known_symb['j'] == 9


def test_TransForTemplateMacro_for_stmt_multi_idx(scope):
    expr = template_macro_parser.parse('for i, j in data.value')
    known_symb = {'data': {'value': [[1, 2], [5, 6], [7, 9]]}}

    transformer = TransForTemplateMacro(scope, known_symb)
    exe = transformer.transform(expr)
    exe.eval()

    assert known_symb['i'] == 7
    assert known_symb['j'] == 9


def test_TransForTemplateMacro_endfor_stmt():
    expr = template_macro_parser.parse('endfor')
    parent = Scope()
    scope = Scope(parent=parent, evalulator=ForStmtEvaluator(0, 0, [], {}))
    transformer = TransForTemplateMacro(scope, {})

    assert transformer.transform(expr) is False
    assert scope == parent


def test_TransForTemplateMacro_endfor_stmt_mismatch(scope):
    expr = template_macro_parser.parse('endfor')
    transformer = TransForTemplateMacro(scope, {})

    with pytest.raises(Exception) as execinfo:
        transformer.transform(expr, lineno=11)

    assert 'Line 11' in str(execinfo.value)


def test_TransForTemplateMacro_if_stmt(scope):
    expr = template_macro_parser.parse('if data.value then')
    known_symb = {'data': {'value': True}}

    transformer = TransForTemplateMacro(scope, known_symb)
    exe = transformer.transform(expr)
    transformer.scope.append(DelayedEvaluator('identity', ('ok',)))
    assert exe.eval() == ['ok']

    assert transformer.scope.parent == scope
    assert transformer.scope.evaluator == exe


def test_TransForTemplateMacro_if_stmt_complex(scope):
    expr = template_macro_parser.parse('if data.value && true then')
    known_symb = {'data': {'value': True}}

    transformer = TransForTemplateMacro(scope, known_symb)
    exe = transformer.transform(expr)
    transformer.scope.append(DelayedEvaluator('identity', ('ok',)))
    assert exe.eval() == ['ok']

    assert transformer.scope.parent == scope
    assert transformer.scope.evaluator == exe


def test_TransForTemplateMacro_elif_stmt():
    expr = template_macro_parser.parse('elif data.value then')
    known_symb = {'data': {'value': True}}

    parent = Scope()
    scope = Scope(parent=parent, evalulator=IfStmtEvaluator(
        DelayedEvaluator("false", ()), []))
    transformer = TransForTemplateMacro(scope, known_symb)
    transformer.transform(expr)
    transformer.scope.append(DelayedEvaluator('identity', ('ok',)))
    exe = scope.evaluator
    assert exe.eval() == ['ok']

    assert transformer.scope.parent == scope
    assert transformer.scope.evaluator == exe


def test_TransForTemplateMacro_elif_stmt_mismatch(scope):
    expr = template_macro_parser.parse('elif true then')
    transformer = TransForTemplateMacro(scope, {})

    with pytest.raises(Exception) as execinfo:
        transformer.transform(expr, lineno=12)

    assert 'Line 12' in str(execinfo.value)


def test_TransForTemplateMacro_else_stmt():
    expr = template_macro_parser.parse('else')

    parent = Scope()
    scope = Scope(parent=parent, evalulator=IfStmtEvaluator(
        DelayedEvaluator("false", ()), []))
    transformer = TransForTemplateMacro(scope, {})
    transformer.transform(expr)
    transformer.scope.append(DelayedEvaluator('identity', ('ok',)))
    exe = scope.evaluator
    assert exe.eval() == ['ok']

    assert transformer.scope.parent == scope
    assert transformer.scope.evaluator == exe


def test_TransForTemplateMacro_else_stmt_mismatch(scope):
    expr = template_macro_parser.parse('else')
    transformer = TransForTemplateMacro(scope, {})

    with pytest.raises(Exception) as execinfo:
        transformer.transform(expr, lineno=12)

    assert 'Line 12' in str(execinfo.value)


def test_TransForTemplateMacro_endif_stmt(scope):
    expr = template_macro_parser.parse('endif')
    parent = Scope()
    scope = Scope(parent=parent, evalulator=IfStmtEvaluator(0, []))
    transformer = TransForTemplateMacro(scope, {})

    assert transformer.transform(expr) is False
    assert scope == parent


def test_TransForTemplateMacro_endif_stmt_mismatch(scope):
    expr = template_macro_parser.parse('endif')
    transformer = TransForTemplateMacro(scope, {})

    with pytest.raises(Exception) as execinfo:
        transformer.transform(expr, lineno=12)

    assert 'Line 12' in str(execinfo.value)
