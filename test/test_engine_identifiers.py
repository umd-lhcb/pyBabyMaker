#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Tue Sep 01, 2020 at 03:07 AM +0800

import pytest

from pyBabyMaker.engine.identifiers import full_line_id, inline_id
from pyBabyMaker.engine.identifiers import Identifier


def test_Identifier_misdef():
    with pytest.raises(AssertionError) as execinfo:
        Identifier('wrong', 'wrong', 2, [False])

    assert "Mismatch" in str(execinfo.value)


def test_full_line_id_no_match():
    assert not full_line_id.search('int a')


def test_full_line_id_match():
    result = full_line_id.search('   // {% for x in data.y %} ')
    assert result
    assert result[1] == '   '
    assert result[2] == 'for x in data.y'
    assert full_line_id.macro_idx == 2


def test_inline_id_no_match():
    assert not inline_id.search('  /* random stuff //')
    assert not inline_id.search('  /* random stuff */')
    assert not inline_id.search('  /* {%} random stuff */')


def test_inline_id_match():
    result = inline_id.search('if(/* {% join: data.y "&&" %} */ )')
    assert result
    assert result[1] == 'if('
    assert result[2] == 'join: data.y "&&"'
    assert result[3] == ' )'
    assert inline_id.macro_idx == 2
