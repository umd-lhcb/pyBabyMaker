#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Sat Aug 29, 2020 at 05:07 PM +0800

from pyBabyMaker.engine.identifiers import full_line_id


def test_full_line_id_no_match():
    assert not full_line_id.search('int a')


def test_full_line_id_match():
    result = full_line_id.search('   // {% for x in data.y %} ')
    assert result
    assert result[1] == '   '
    assert result[2] == 'for x in data.y'
