#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Tue Sep 01, 2020 at 03:40 AM +0800

from pyBabyMaker.engine.core import template_transformer, template_evaluator


def test_template_transformer_trivial_line():
    file_content = [
        'int a = 1;\n'
    ]
    result = template_transformer(file_content, {})
    assert template_evaluator(result) == ['int a = 1;\n']


def test_template_evaluator_simple_replacement():
    file_content = [
        'int a = 1;\n',
        '    // {% directive.b %}\n'
    ]
    result = template_transformer(file_content, {'b': 1})
    assert template_evaluator(result) == ['int a = 1;\n', '    1\n']
