#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Tue Sep 01, 2020 at 04:30 AM +0800

import pytest

from pyBabyMaker.engine.core import helper_flatten
from pyBabyMaker.engine.core import template_transformer, template_evaluator


def test_helper_flatten_trivial():
    assert helper_flatten([1, 2, 3]) == [1, 2, 3]


def test_helper_flatten_complex():
    assert helper_flatten([1, [2, [3, 4, 5, [6, 7]]], 8]) == list(range(1, 9))


def test_helper_flatten_corner_case1():
    assert helper_flatten([[1, [2, 3, 4, [5, 6]]]]) == list(range(1, 7))


def test_template_transformer_trivial_line():
    file_content = [
        'int a = 1;\n'
    ]
    result = template_transformer(file_content, {})
    assert template_evaluator(result) == ['int a = 1;\n']


def test_template_evaluator_full_line_simple():
    file_content = [
        'int a = 1;\n',
        '    // {% directive.b %}\n'
    ]
    result = template_transformer(file_content, {'b': 1})
    assert template_evaluator(result) == ['int a = 1;\n', '    1\n']


def test_template_evaluator_inline_simple():
    file_content = [
        'int a = 1;\n',
        '    if(/* {% directive.b %}  */  )\n'
    ]
    result = template_transformer(file_content, {'b': 1})
    assert template_evaluator(result) == ['int a = 1;\n',
                                          '    if(1  )\n']


def test_template_evaluator_for_stmt_simple():
    file_content = [
        '// {% for i in directive.b %}\n',
        'cout << "Random stuff";\n',
        'cout << /* {% i %} */ ;\n'
    ]
    result = template_transformer(file_content, {'b': [1, 2, 3]}, False)
    assert template_evaluator(result) == [
        'cout << "Random stuff";\n',
        'cout << 1 ;\n'
        'cout << "Random stuff";\n',
        'cout << 2 ;\n'
        'cout << "Random stuff";\n',
        'cout << 3 ;\n'
    ]
