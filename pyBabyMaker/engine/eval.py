#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Mon Aug 31, 2020 at 05:08 AM +0800
"""
This module provide template macro evaluation.
"""

from .functions import macro_funcs


class DelayedEvaluator(object):
    """
    General container for storing info needed for executing macro at a later
    stage.

    :param str func_name: function name. Must be defined in ``macro_funcs``.
    :param tuple/list args: function arguments.
    """
    def __init__(self, func_name, args):
        try:
            self.func = macro_funcs[func_name]
        except KeyError:
            raise KeyError('Unknown function: {}'.format(func_name))

        self.args = args

    def eval(self):
        args_eval = [arg.eval() if hasattr(arg, 'eval') else arg
                     for arg in self.args]
        return self.func(*args_eval)
