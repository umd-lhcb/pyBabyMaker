#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Tue Sep 01, 2020 at 05:32 PM +0800

import pytest

from lark.exceptions import UnexpectedToken
from pyBabyMaker.engine.syntax import template_macro_parser


def test_for_stmt_simple():
    assert template_macro_parser.parse('for h in data').pretty() == \
        "for_stmt\n" \
        "  h\n" \
        "  var\tdata\n"


def test_for_stmt_complex():
    assert template_macro_parser.parse('for h in data.value').pretty() == \
        "for_stmt\n" \
        "  h\n" \
        "  getattr\n" \
        "    var\tdata\n" \
        "    value\n"


def test_for_stmt_multi_idx():
    assert template_macro_parser.parse('for i, j in data').pretty() == \
        "for_stmt\n" \
        "  i\n" \
        "  j\n" \
        "  var\tdata\n"


def test_endfor_valid():
    assert template_macro_parser.parse('endfor').pretty() == 'endfor_stmt\n'


def test_endfor_invalid():
    with pytest.raises(UnexpectedToken) as execinfo:
        template_macro_parser.parse('endfor x')

    assert 'Expected one of' in str(execinfo.value)


def test_getattr():
    assert template_macro_parser.parse('x.y').pretty() == \
        "getattr\n" \
        "  var\tx\n" \
        "  y\n"


def test_getitem_var():
    assert template_macro_parser.parse('x[y]').pretty() == \
        "getitem\n" \
        "  var\tx\n" \
        "  var\ty\n"


def test_getitem_num():
    assert template_macro_parser.parse('x[1]').pretty() == \
        "getitem\n" \
        "  var\tx\n" \
        "  num\t1\n"


def test_method_call():
    assert template_macro_parser.parse('data->m: a, b').pretty() == \
        "method_call\n" \
        "  var\tdata\n" \
        "  m\n" \
        "  arguments\n" \
        "    var\ta\n" \
        "    var\tb\n"


def test_method_call_no_arg():
    assert template_macro_parser.parse('data->m:').pretty() == \
        "method_call\n" \
        "  var\tdata\n" \
        "  m\n"


def test_func_call():
    assert template_macro_parser.parse('f: x, y').pretty() == \
        "func_call\n" \
        "  f\n" \
        "  arguments\n" \
        "    var\tx\n" \
        "    var\ty\n"


def test_func_call_nested():
    assert template_macro_parser.parse('f: (x: z, 1), y, 21').pretty() == \
        "func_call\n" \
        "  f\n" \
        "  arguments\n" \
        "    func_call\n" \
        "      x\n" \
        "      arguments\n" \
        "        var\tz\n" \
        "        num\t1\n" \
        "    var\ty\n" \
        "    num\t21\n"
