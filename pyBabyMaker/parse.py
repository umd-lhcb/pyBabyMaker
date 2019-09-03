#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Tue Sep 03, 2019 at 05:58 PM -0400

import re


def is_numeral(n):
    try:
        float(n)
        return True
    except ValueError:
        return False


def find_all_args(s, tokens=[
    r'[\w\d_].*\(',
    r'\(', r'\)', r',',
    r'\+', r'-', r'\*', r'/', r'%',
    r'&&', r'\|\|', r'!'
]):
    for t in tokens:
        s = re.sub(t, ' ', s)
        print(s)
    return s.split()
