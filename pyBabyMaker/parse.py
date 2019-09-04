#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Wed Sep 04, 2019 at 12:36 AM -0400
"""
This module provides limited functionality to extract variables from certain
type of C++ expressions.

Currently, supported C++ expressions includes arithmetic and boolean calculation
and nested function calls.
"""

import re


def is_numeral(n):
    """
    Test if ``string n`` can be converted to a numeral.
    """
    try:
        float(n)
        return True
    except ValueError:
        return False


def find_all_args(s, tokens=[
    r'[\w\d_]*\(', r'\)', r',',
    r'\+', r'-', r'\*', r'/', r'%',
    r'&&', r'\|\|',
    r'!', r'>', r'<', r'='
]):
    """
    Find all arguments inside a C++ expression ``s``.
    """
    for t in tokens:
        s = re.sub(t, ' ', s)
    return s.split()


def find_all_vars(s, **kwargs):
    """
    Find all arguments, minus numerals, inside a C++ expression ``s``.
    """
    args = find_all_args(s, **kwargs)
    return [v for v in args if not is_numeral(v)]
