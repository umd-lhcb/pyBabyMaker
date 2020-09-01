#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Tue Sep 01, 2020 at 05:07 PM +0800
"""
This module provide a parser for template macros extracted from C++ files.
"""

from lark import Lark


template_macro_grammar = '''
    ?start: stmt

    ?stmt: for_stmt | endfor_stmt | atom_expr

    for_stmt: "for" NAME ("," NAME)* "in" atom_expr

    endfor_stmt: "endfor"

    ?atom_expr: NAME ":" [arguments]             -> func_call
        | atom_expr "[" atom_expr "]"            -> getitem
        | atom_expr "." NAME                     -> getattr
        | atom_expr "->" NAME ":" [arguments]    -> method_call
        | atom

    ?atom: NUMBER    -> num
        | "-"atom    -> neg
        | BOOL       -> bool
        | NAME       -> var
        | STRING     -> str
        | "(" atom_expr ")"

    arguments: (atom_expr ",")* (atom_expr [","])

    %import common.SIGNED_NUMBER -> NUMBER
    %import common.CNAME -> NAME
    %import common.WS_INLINE
    %import common.ESCAPED_STRING -> _STRING

    %ignore WS_INLINE

    STRING: _STRING "i"?
    BOOL.2: "True" | "False" | "true" | "false"  // these have higher priority
'''

template_macro_parser = Lark(template_macro_grammar, parser='lalr')
