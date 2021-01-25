#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Mon Jan 25, 2021 at 01:12 AM +0100
"""
This module provide a parser for template macros extracted from C++ files.

A compromise is made to **NOT** support arithmetic operations at syntax level.
If you need that, define your own functors.

This is because there's a conflict in the LALR(1) resolution when having both
*subtraction* (``a-b``, where ``-`` is a binary operator) and *negation*
(``-a``, where ``-`` an unary operator).

We also choose to **NOT** parse ``if`` and ``for`` statements as a unified
block. This is because the parser works on a line-by-line basis---it doesn't
have access to the whole "macro" source code.
"""

from lark import Lark


template_macro_grammar = '''
    ?start: for_stmt | endfor_stmt
        | if_stmt | elif_stmt | else_stmt | endif_stmt
        | boolor

    if_stmt: "if" boolor "then"
    elif_stmt: "elif" boolor "then"
    else_stmt: "else"
    endif_stmt: "endif"

    for_stmt: "for" NAME ("," NAME)* "in" molecule
    endfor_stmt: "endfor"

    ?boolor: booland
        | boolor "||" booland -> op_or

    ?booland: cond  // '&' binds tigher than '|'
        | booland "&&" cond -> op_and

    ?cond: molecule
        | cond "==" molecule    -> eq
        | cond "!=" molecule    -> neq
        | cond ">"  molecule    -> gt
        | cond ">=" molecule    -> gte
        | cond "<"  molecule    -> lt
        | cond "<=" molecule    -> lte

    ?molecule: NAME ":" [arguments]             -> func_call
        | molecule "[" molecule "]"             -> getitem
        | molecule "." NAME                     -> getattr
        | molecule "->" NAME ":" [arguments]    -> method_call
        | atom

    ?atom: NUMBER    -> num
        | "-" atom   -> neg
        | BOOL       -> bool
        | NAME       -> var
        | STRING     -> str
        | "(" boolor ")"

    arguments: (boolor ",")* (boolor [","])

    %import common.SIGNED_NUMBER -> NUMBER
    %import common.WS_INLINE
    %import common.CNAME -> NAME
    %import common.ESCAPED_STRING -> _STRING

    %ignore WS_INLINE

    STRING: _STRING "i"?
    BOOL.2: "True" | "False" | "true" | "false"  // these have higher priority
'''

template_macro_parser = Lark(template_macro_grammar, parser='lalr', debug=True)
