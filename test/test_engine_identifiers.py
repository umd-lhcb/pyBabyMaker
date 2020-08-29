#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Sat Aug 29, 2020 at 05:28 PM +0800

from pyBabyMaker.engine.identifiers import full_line_id, inline_id


def test_full_line_id_no_match():
    assert not full_line_id.search('int a')


def test_full_line_id_match():
    result = full_line_id.search('   // {% for x in data.y %} ')
    assert result
    assert result[1] == '   '
    assert result[2] == 'for x in data.y'


def test_inline_id_no_match():
    assert not inline_id.search('  /* random stuff //')


def test_inline_id_match():
    result = inline_id.search('if(/* {% join: data.y "&&" %} */ )')
    assert result
    assert result[1] == 'if('
    assert result[2] == 'join: data.y "&&"'
    assert result[3] == ' )'
