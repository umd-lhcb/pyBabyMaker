#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Mon Aug 31, 2020 at 04:57 PM +0800
"""
This module provide template macro evaluation.
"""

from lark import Transformer, v_args
from .functions import macro_funcs


class DelayedEvaluator(object):
    """
    General container for storing info needed for executing macro at a later
    stage.
    """
    def __init__(self, func_name, args):
        """
        Initialize evaluator.

        :param str func_name: function name. Must be defined in ``macro_funcs``.
        :param tuple/list args: function arguments.
        """
        try:
            self.func = macro_funcs[func_name]
        except KeyError:
            raise KeyError('Unknown function: {}'.format(func_name))

        self.args = args

    def eval(self):
        """
        Evaluate stored functions and all its arguments recursively.
        """
        args_eval = [arg.eval() if hasattr(arg, 'eval') else arg
                     for arg in self.args]
        return self.func(*args_eval)


class TransForTemplateMacro(Transformer):
    """
    Transformer for template macro.
    """
    def __init__(self, scope, known_symb, known_funcs=macro_funcs):
        self.scope = scope
        self.known_symb = known_symb
        self.known_funcs = known_funcs

    ########
    # atom #
    ########

    @v_args(inline=True)
    def num(self, val):
        try:
            return int(val)
        except ValueError:
            return float(val)

    @v_args(inline=True)
    def bool(self, val):
        return True if val.lower() == 'true' else False

    @v_args(inline=True)
    def neg(self, val):
        return -val

    @v_args(inline=True)
    def str(self, val):
        return val.replace('"', '')

    @v_args(inline=True)
    def var(self, val):
        return self.known_symb[val]
