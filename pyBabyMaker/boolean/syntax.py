#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Fri Sep 18, 2020 at 05:38 PM +0800
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

    ?molecule: NAME "(" [arguments] ")"           -> func_call
        | molecule "." NAME                       -> getattr
        | molecule "->" NAME                      -> getattr
        | molecule "." NAME "(" [arguments] ")"   -> method_call
        | molecule "->" NAME "(" [arguments] ")"  -> method_call
        | atom

    ?atom: NUMBER     -> num
        | "-" atom    -> neg
        | BOOL        -> bool
        | NAME        -> var
        | "(" boolor ")"

    arguments: (boolor ",")* (boolor [","])

    %import common.SIGNED_NUMBER -> NUMBER
    %import common.WS_INLINE
    %import common.CNAME -> NAME

    %ignore WS_INLINE

    BOOL.2: "true" | "false"  // These keywords have higher priority
'''

cpp_boolean_parser = Lark(cpp_boolean_grammar, parser='lalr')
