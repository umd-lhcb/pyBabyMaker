#!/usr/bin/env python
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Sun Aug 30, 2020 at 04:48 AM +0800
"""
This module provide a parser for template macros extracted from C++ files.
"""

from lark import Lark


template_macro_grammar = '''
    ?start: for_stmt

    for_stmt: "for" atom_expr "in" atom_expr

    ?atom_expr: atom_expr ":" [arguments]    -> func_call
          | atom_expr "[" atom_expr "]"      -> getitem
          | atom_expr "." NAME               -> getattr
          | atom

    ?atom: NUMBER    -> num
        | "-"atom    -> neg
        | BOOL       -> bool
        | NAME       -> var
        | "(" atom_expr ")"

    arguments: (atom_expr " ")* (atom_expr [" "])

    %import common.SIGNED_NUMBER -> NUMBER
    %import common.CNAME -> NAME

    %ignore /[\t \f]+/  // white space

    BOOL.2: "True" | "False" | "true" | "false"  // these have higher priority
'''

template_macro_parser = Lark(template_macro_grammar, parser='lalr')
