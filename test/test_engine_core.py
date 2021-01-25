#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Mon Jan 25, 2021 at 05:15 AM +0100

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
        'cout << /* {% i %} */ ;\n',
    ]
    result = template_transformer(file_content, {'b': [1, 2, 3]}, False)
    assert template_evaluator(result.parent) == [
        'cout << "Random stuff";\n',
        'cout << 1 ;\n',
        'cout << "Random stuff";\n',
        'cout << 2 ;\n',
        'cout << "Random stuff";\n',
        'cout << 3 ;\n'
    ]


def test_template_evaluator_for_stmt_nested():
    file_content = [
        '// {% for i in directive.b %}\n',
        'cout << "Random stuff";\n',
        '// {% for j in i.stuff %}\n',
        '  cout << /* {% j %} */ ;\n',
        '// {% endfor %}\n',
        '// {% endfor %}\n'
    ]
    result = template_transformer(
        file_content,
        {'b': [{'stuff': [1, 2]}, {'stuff': [3]}, {'stuff': [4, 5, 6]}]})
    assert template_evaluator(result) == [
        'cout << "Random stuff";\n',
        '  cout << 1 ;\n',
        '  cout << 2 ;\n',
        'cout << "Random stuff";\n',
        '  cout << 3 ;\n',
        'cout << "Random stuff";\n',
        '  cout << 4 ;\n',
        '  cout << 5 ;\n',
        '  cout << 6 ;\n'
    ]


def test_template_evaluator_for_stmt_multi_idx():
    file_content = [
        '// {% for key, val in directive.b->items: %}\n',
        '  cout << /* {% format: "{} = {}", key, val %} */ <<endl;\n'
    ]
    result = template_transformer(
        file_content,
        {'b': {'a': 1, 'b': 2, 'c': 3}},
        False)
    assert template_evaluator(result.parent) == [
        '  cout << a = 1 <<endl;\n',
        '  cout << b = 2 <<endl;\n',
        '  cout << c = 3 <<endl;\n',
    ]


def test_template_transformer_for_stmt_mismatch():
    file_content = [
        '// {% for key, val in directive.b->items: %}\n',
        '  cout << /* {% format: "{} = {}", key, val %} */ <<endl;\n'
    ]
    with pytest.raises(ValueError) as execinfo:
        template_transformer(file_content, {'b': {'a': 1, 'b': 2}})

    assert 'Unclosed for statement\n' == str(execinfo.value)


def test_template_evaluator_for_stmt_proper():
    file_content = [
        '// {% for key, val in directive.b->items: %}\n',
        '  cout << /* {% key %} */ <<endl;\n',
        '  // {% for v in val %}',
        '    cout << /* {% v %} */ <<endl;\n',
        '  // {% endfor %}\n',
        '  cout << "stuff" <<endl;\n',
        '// {% endfor %}\n',
    ]
    result = template_transformer(
        file_content,
        {'b': {'a': [1, 2], 'b': [3, 4, 5], 'c': [6]}},
        False)
    assert template_evaluator(result) == [
        '  cout << a <<endl;\n',
        '    cout << 1 <<endl;\n',
        '    cout << 2 <<endl;\n',
        '  cout << "stuff" <<endl;\n',
        '  cout << b <<endl;\n',
        '    cout << 3 <<endl;\n',
        '    cout << 4 <<endl;\n',
        '    cout << 5 <<endl;\n',
        '  cout << "stuff" <<endl;\n',
        '  cout << c <<endl;\n',
        '    cout << 6 <<endl;\n',
        '  cout << "stuff" <<endl;\n',
    ]


def test_template_evaluator_if_stmt_proper():
    file_content = [
        'cout << /* {% directive.B %} */ <<endl;\n',
        '// {% if directive.a && true then %}\n',
        '  cout << /* {% directive.A %} */ <<endl;\n',
        '// {% endif %}\n',
    ]

    # Case 1
    known_symb = {'a': True, 'A': 1, 'B': 2, 'C': 3}
    result = template_transformer(file_content, known_symb)
    assert template_evaluator(result) == [
        'cout << 2 <<endl;\n',
        '  cout << 1 <<endl;\n',
    ]

    # Case 2
    known_symb = {'a': False, 'A': 1, 'B': 2, 'C': 3}
    result = template_transformer(file_content, known_symb)
    assert template_evaluator(result) == [
        'cout << 2 <<endl;\n',
    ]


def test_template_evaluator_if_stmt_proper_complex():
    file_content = [
        '// {% if directive.a && true then %}\n',
        '  cout << /* {% directive.A %} */ <<endl;\n',
        '  cout << /* {% directive.B %} */ <<endl;\n',
        '  cout << /* {% directive.C %} */ <<endl;\n',
        '// {% elif directive.b || false then  %}\n',
        '  cout << /* {% directive.B %} */ <<endl;\n',
        '// {% else %}\n',
        '  cout << /* {% directive.C %} */ <<endl;\n',
        '// {% endif %}\n',
    ]

    # Case 1
    known_symb = {'a': True, 'b': True, 'A': 1, 'B': 2, 'C': 3}
    result = template_transformer(file_content, known_symb)
    assert template_evaluator(result) == [
        '  cout << 1 <<endl;\n',
        '  cout << 2 <<endl;\n',
        '  cout << 3 <<endl;\n',
    ]

    # Case 2
    known_symb = {'a': False, 'b': True, 'A': 1, 'B': 2, 'C': 3}
    result = template_transformer(file_content, known_symb)
    assert template_evaluator(result) == [
        '  cout << 2 <<endl;\n',
    ]

    # Case 3
    known_symb = {'a': False, 'b': False, 'A': 1, 'B': 2, 'C': 3}
    result = template_transformer(file_content, known_symb)
    assert template_evaluator(result) == [
        '  cout << 3 <<endl;\n',
    ]
