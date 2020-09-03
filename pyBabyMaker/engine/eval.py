#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Fri Sep 04, 2020 at 04:27 AM +0800
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

        for loop_var in self.iterable.eval():
            # Set up loop variables in the global scope (known_symb)
            if len(self.idx) > 1:  # unpack only if more than one loop variable
                for i, var_name in enumerate(self.idx):
                    self.known_symb[var_name] = loop_var[i]
            else:
                self.known_symb[self.idx[0]] = loop_var

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
        # First, remove the literal " at string boundaries
        val = val[1:-1]
        # Now replace escaped UNIX EOL with regular EOL
        for src, dst in (
            ('\\"', '"'),    # escaped "
            ('\\n', '\n'),   # escaped \n
        ):
            val = val.replace(src, dst)
        return val

    #######################
    # Delayed evaluations #
    #######################

    @v_args(inline=True)
    def var(self, val):
        return DelayedEvaluator('val', (val, self.known_symb))

    @v_args(inline=True)
    def neg(self, val):
        return DelayedEvaluator('neg', (val,))

    ########################
    # Function/method call #
    ########################

    @v_args(inline=True)
    def func_call(self, func_name, arguments=None):
        args = arguments.children if arguments is not None else []
        return DelayedEvaluator(str(func_name), args)

    @v_args(inline=True)
    def method_call(self, instance, method_name, arguments=None):
        args = arguments.children if arguments is not None else []
        return DelayedEvaluator('method_call', (instance, method_name, *args))

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
    def for_stmt(self, *args):
        idx = [str(i) for i in args[:-1]]
        iterable = args[-1]

        self.stmt_counters['for'] += 1
        return ForStmtEvaluator(idx, iterable, self.scope, self.known_symb)

    @v_args(inline=True)
    def endfor_stmt(self):
        self.stmt_counters['for'] -= 1

        if self.stmt_counters['for'] >= 0:
            return self.scope.pop()
        else:
            raise ValueError('Line {}: Unmatched "endfor" statement.'.format(
                self.lineno))
