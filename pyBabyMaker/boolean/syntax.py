#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Tue Aug 10, 2021 at 03:47 PM +0200
"""
This module defines C++ boolean syntax.
"""

from lark import Lark


cpp_boolean_grammar = '''
    ?start: boolor

    ?boolor: booland
        | boolor "||" booland -> op_or

    ?booland: cond  // '&' binds tigher than '|'
        | booland "&&" cond -> op_and

    ?cond: expr
        | cond "==" expr    -> eq
        | cond "!=" expr    -> neq
        | cond ">"  expr    -> gt
        | cond ">=" expr    -> gte
        | cond "<"  expr    -> lt
        | cond "<=" expr    -> lte

    ?expr: sum
        | "!" sum -> comp  // logical complement

    ?sum: product
        | sum "+" product    -> add
        | sum "-" product    -> sub

    ?product: molecule
        | product "*" molecule   -> mul
        | product "/" molecule   -> div

    ?molecule: NAME "(" [arguments] ")"             -> func_call
        | NAME "{" [arguments] "}"                  -> func_call
        | fullname "(" [arguments] ")"              -> func_call
        | fullname "{" [arguments] "}"              -> func_call
        | molecule "." NAME                         -> getattr
        | molecule "->" NAME                        -> getattr
        | molecule "." NAME "(" [arguments] ")"     -> method_call
        | molecule "->" NAME "(" [arguments] ")"    -> method_call
        | atom

    ?atom: NUMBER     -> num
        | "-" atom    -> neg
        | BOOL        -> bool
        | NAME        -> var
        | fullname    -> var
        | "(" boolor ")"

    arguments: (boolor ",")* (boolor [","])
    fullname: (NAME "::")+ NAME

    %import common.SIGNED_NUMBER -> RAW_NUM
    %import common.WS_INLINE
    %import common.CNAME -> NAME

    %ignore WS_INLINE

    NUMBER: RAW_NUM NUM_SUFFIX*
    NUM_SUFFIX: "f" | "F" | "u" | "U" | "ll" | "LL" | "l" | "L"
    BOOL.2: "true" | "false"  // These keywords have higher priority
'''

cpp_boolean_parser = Lark(cpp_boolean_grammar, parser='lalr')
