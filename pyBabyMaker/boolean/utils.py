#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Thu Sep 03, 2020 at 11:51 PM +0800
"""
This module provides simple parsed boolean tree info extraction
"""

from .syntax import cpp_boolean_parser as cpp


def find_all_args(expr):
    """
    Find all function call arguments in the expression.

    :param str expr: Expression to be parsed
    """
    tree = cpp.parse(expr)
    args = tree.find_data('arguments')
    result = []

    for subtree in args:
        result += [t.children[0].value for t in subtree.find_data('var')]

    return result


def find_all_vars(expr):
    """
    Find all variables, include function arguments, in the expression.

    :param str expr: Expression to be parsed
    """
    tree = cpp.parse(expr)
    return [t.children[0].value for t in tree.find_data('var')]
