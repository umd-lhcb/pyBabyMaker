#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Wed Sep 09, 2020 at 03:06 AM +0800
"""
This module defines functions for template macro.
"""

import re

from datetime import datetime

from pyBabyMaker.base import UniqueList
from pyBabyMaker.boolean.utils import find_all_vars


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

    :param Any val: an object that either has attribute ``attr`` or is a dict
                    and has a key named ``attr``
    :param str attr: name of the attribute/dict key.
    """
    try:
        return getattr(val, str(attr))
    except Exception:
        return val[str(attr)]


def func_deref_var(expr, vars_to_deref):
    """
    Dereference variables loaded from ntuple directly. For example:

    .. code-block:: c++

       TTreeReader reader("tree", input_file)
       TTreeReaderValue<double> Y_PT(reader, "Y_PT");
       while (reader.Next()) {
         cout << (*Y_PT)
       }

    The ``Y_PT`` inside the ``while`` loop needs to be dereferenced.

    :param str expr: C++ expression that has variables to be dereferenced.
    :param list vars_to_deref: list of variables to be dereferenced.
    """
    variables = UniqueList(find_all_vars(expr))

    for v in variables:
        if v in vars_to_deref:
            expr = re.sub(r'\b'+v+r'\b', '(*{})'.format(v), expr)

    return expr


def func_format_list(str_template, lst):
    """
    Return attribute if it exists; otherwise treat attribute as a dict key.

    :param str str_template: string template to be formatted.
    :param list lst: list of arguments to be used to format string template.
    """
    args = [[a] if not isinstance(a, list) else a for a in lst]
    return [str_template.format(*a) for a in args]


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
    'method_call': lambda instance, method_name, *args:
        getattr(instance, method_name)(*args),
    'gendate': lambda fmt='%Y-%m-%d %H:%M:%S.%f': '// Generated on: {}'.format(
        datetime.now().strftime(fmt)),
    'deref_var': func_deref_var,
    'format_list': func_format_list,
    'deref_var_list': lambda expr_lst, vars_to_deref:
        ['({})'.format(func_deref_var(expr, vars_to_deref))
         for expr in expr_lst],
}
