#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Fri Aug 28, 2020 at 07:15 PM +0800

from pyBabyMaker.engine.identifiers import full_line_id


def test_full_line_id():
    assert full_line_id.search('int a') is None
