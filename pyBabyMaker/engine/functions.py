#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Mon Aug 31, 2020 at 05:19 PM +0800
"""
This module defines functions for template macro.
"""


def func_input(path):
    """
    Macro function to read literal input from `path`.

    :param str/pathlib.Path path: path to the input file.
    """
    with open(path) as f:
        return f.readlines()


macro_funcs = {
    'identity': lambda x: x,
    'join': lambda lst, string: string.join(lst),
    'input': func_input,
    'one': lambda: 1,
}
