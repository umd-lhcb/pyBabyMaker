#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Sat Aug 29, 2020 at 04:45 PM +0800

from pyBabyMaker.engine.identifiers import full_line_id


def test_full_line_id_no_match():
    assert full_line_id.search('int a') is None


def test_full_line_id_match():
    result = full_line_id.search('   // {% for x in data.y %} ')
    assert result is not None
    assert result.group(1) == '   '
    assert result.group(2) == 'for x in data.y '
