#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Tue Sep 01, 2020 at 04:13 AM +0800
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


class ForStmtEvaluator(object):
    """
    General container for storing info needed for executing macro at a later
    stage.
    """
    def __init__(self, idx, iterable, scope, known_symb):
        """
        Initialize for-statement evaluator.

        :param str idx: name of the loop variable.
        :param DelayedEvaluator iterable: iterable in the for-loop.
        """
        self.eval_list = []
        scope.append(self.eval_list)

        self.idx = idx
        self.iterable = iterable

        self.known_symb = known_symb

    def eval(self):
        """
        Evaluate for-loop and all evaluable in its scope.
        """
        out = []

        for i in self.iterable.eval():
            self.known_symb[self.idx] = i
            for evaluator in self.eval_list:
                out.append(evaluator.eval())

        return out


class TransForTemplateMacro(Transformer):
    """
    Transformer for template macro.
    """
    def __init__(self, scope, known_symb):
        self.scope = scope
        self.known_symb = known_symb
        self.stmt_counters = {'for': 0}
        self.lineno = 0

    ###########
    # General #
    ###########

    def transform(self, *args, lineno=0, **kwargs):
        self.lineno = lineno
        return super().transform(*args, **kwargs)

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
    def str(self, val):
        return val.replace('"', '')

    #######################
    # Delayed evaluations #
    #######################

    @v_args(inline=True)
    def var(self, val):
        return DelayedEvaluator('val', (val, self.known_symb))

    @v_args(inline=True)
    def neg(self, val):
        return DelayedEvaluator('neg', (val,))

    #################
    # Function call #
    #################

    @v_args(inline=True)
    def func_call(self, func_name, arguments=None):
        args = arguments.children if arguments is not None else []
        return DelayedEvaluator(str(func_name), args)

    ###########
    # Getters #
    ###########

    @v_args(inline=True)
    def getattr(self, val, attr):
        return DelayedEvaluator('getattr', (val, attr))

    @v_args(inline=True)
    def getitem(self, val, key):
        return DelayedEvaluator('getitem', (val, key))

    ##############
    # Statements #
    ##############

    @v_args(inline=True)
    def for_stmt(self, idx, iterable):
        self.stmt_counters['for'] += 1
        return ForStmtEvaluator(idx, iterable, self.scope, self.known_symb)

    @v_args(inline=True)
    def endfor_stmt(self):
        self.stmt_counters['for'] -= 1

        if self.stmt_counters['for'] >= 0:
            return self.scope.pop()
        else:
            raise ValueError('Line {}: Unmatched "endfor" statement.'.format(
                self.lineno
            ))
