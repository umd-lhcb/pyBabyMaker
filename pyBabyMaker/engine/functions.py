#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Sat Jun 19, 2021 at 03:55 AM +0200
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
    except AttributeError:
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


def func_guard(input_str, chars_to_replace=['*', '/']):
    """
    Return a string with chars illegal in variable names replaced.

    :param str input_str: string to be replaced.
    :param list chars_to_replace: list of illegal chars.
    """
    for c in chars_to_replace:
        input_str = input_str.replace(c, '_')
    return input_str


def _func_wrapper(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print('Error when executing function: {}'.format(f.__name__))
            print('The arguments are: {}'.format(', '.join(
                [str(i) for i in args]
            )))
            print('The keyword arguments are: {}'.format(', '.join(
                ['{}={}'.format(k, str(kwargs[k])) for k in kwargs]
            )))
            raise e

    return inner


macro_funcs_raw = {
    # Trivial
    'identity': lambda x: x,
    'one': lambda: 1,
    # Boolean
    'true': lambda: True,
    'false': lambda: False,
    # IO
    'input': func_input,
    # List & dict
    'join': lambda lst, string: string.join(lst),
    'list': lambda *args: [i for i in args],
    'pop': lambda lst: lst.pop() if lst else None,
    'enum': lambda lst, start=0: enumerate(lst, start=start),
    # Arithmetic
    'neg': lambda val: -val,
    # Boolean
    'comp': lambda cond: not cond,
    'eq': lambda lhs, rhs: lhs == rhs,
    'gt': lambda lhs, rhs: lhs > rhs,
    'gte': lambda lhs, rhs: lhs >= rhs,
    'lt': lambda lhs, rhs: lhs < rhs,
    'lte': lambda lhs, rhs: lhs <= rhs,
    'and': lambda cond1, cond2: cond1 and cond2,
    'or': lambda cond1, cond2: cond1 or cond2,
    # Attribute getters
    'val': lambda val, attrs: attrs[val],
    'getattr': func_getattr,
    'getitem': lambda val, key: val[key],
    # String manipulation
    'format': lambda str_template, *args: str_template.format(*args),
    'format_list': func_format_list,
    'quote': lambda s: '"{}"'.format(s),
    'guard': func_guard,
    # Function/Method callers
    'method_call': lambda instance, method_name, *args:
        getattr(instance, method_name)(*args),
    # Aux
    'gendate': lambda fmt='%Y-%m-%d %H:%M:%S.%f': '// Generated on: {}'.format(
        datetime.now().strftime(fmt)),
    'deref_var': func_deref_var,
    'deref_var_list': lambda expr_lst, vars_to_deref:
        ['({})'.format(func_deref_var(expr, vars_to_deref))
         for expr in expr_lst],
    # C++ shorthands
    'declare': lambda t, n: "{} {};".format(t, n),
    'assign': lambda lval, rval: "{} = {};".format(lval, rval),
}

macro_funcs = {k: _func_wrapper(f) for k, f in macro_funcs_raw.items()}
