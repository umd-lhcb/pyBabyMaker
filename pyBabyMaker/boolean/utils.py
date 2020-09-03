#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Thu Sep 03, 2020 at 11:32 PM +0800
"""
This module provides simple parsed boolean tree info extraction
"""


def find_all_args(tree):
    """
    Find all function call arguments in the parse tree.

    :param Any tree: Parsed AST generated with ``lark``.
    """
    args = tree.find_data('arguments')
    result = []

    for subtree in args:
        result += [t.children[0].value for t in subtree.find_data('var')]

    return result


def find_all_vars(tree):
    """
    Find all variables, include function arguments, in the parse tree.

    :param Any tree: Parsed AST generated with ``lark``.
    """
    return [t.children[0].value for t in tree.find_data('var')]
