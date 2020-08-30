#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Mon Aug 31, 2020 at 02:10 AM +0800

import pytest

from lark.exceptions import UnexpectedToken
from pyBabyMaker.engine.macro_parse import template_macro_parser


def test_for_stmt_simple():
    assert template_macro_parser.parse('for h in data').pretty() == \
        "for_stmt\n" \
        "  var\th\n" \
        "  var\tdata\n"


def test_for_stmt_complex():
    assert template_macro_parser.parse('for h in data.value').pretty() == \
        "for_stmt\n" \
        "  var\th\n" \
        "  getattr\n" \
        "    var\tdata\n" \
        "    value\n"


def test_endfor_valid():
    assert template_macro_parser.parse('endfor').pretty() == 'endfor_stmt\n'


def test_endfor_invalid():
    with pytest.raises(UnexpectedToken) as execinfo:
        template_macro_parser.parse('endfor x')

    assert 'Expected one of' in str(execinfo.value)
