#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Tue Sep 01, 2020 at 02:12 AM +0800
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


def func_getattr(val, attr):
    """
    Return attribute if it exists; otherwise treat attribute as a dict key.

    :param Any val: an object that either has attribute ``attr`` or is a dict and
                    has a key named ``attr``
    :param str attr: name of the attribute/dict key.
    """
    try:
        return getattr(val, str(attr))
    except Exception:
        return val[str(attr)]


macro_funcs = {
    'identity': lambda x: x,
    'join': lambda lst, string: string.join(lst),
    'input': func_input,
    'one': lambda: 1,
    'list': lambda *args: [i for i in args],
    'val': lambda val, attrs: attrs[val],
    'neg': lambda val: -val,
    'getattr': func_getattr,
    'getitem': lambda val, key: val[key],
    'format': lambda str_template, *args: str_template.format(*args),
    'pop': lambda lst: lst.pop() if lst else None,
}
