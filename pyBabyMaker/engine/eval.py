#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Mon Jan 25, 2021 at 05:13 AM +0100
"""
This module provide template macro evaluation.
"""

from lark import Transformer, v_args
from .functions import macro_funcs


class Scope(list):
    def __init__(self, iterable=[], parent=None, evalulator=None):
        self.parent = parent
        self.evaluator = evalulator
        super().__init__(iterable)


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
    Delayed evaluator for ``for ... endfor`` statement.
    """
    def __init__(self, idx, iterable, loop, known_symb):
        """
        Initialize for-statement evaluator.

        :param str idx: name of the loop variable.
        :param DelayedEvaluator iterable: the object to be iterated over.
        :param list loop: empty list to store evaluators in the for loop.
        :param dict known_symb: all known symbols.
        """
        self.idx = idx
        self.iterable = iterable
        self.loop = loop
        self.known_symb = known_symb
        self.name = 'for'

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

            for evaluator in self.loop:
                out.append(evaluator.eval())

        return out


class IfStmtEvaluator(object):
    """
    Delayed evaluator for ``if ... (elif ... else ...) fi`` statements.
    """
    def __init__(self, cond, branch):
        """
        Initialize if-statements evaluator.

        :param DelayedEvaluator cond: conditional.
        :param list branch: empty list to store evaluators in the if branch.
        """
        self.conds = [(cond, branch)]
        self.name = 'if'

    def add_cond(self, cond, branch):
        """
        Add an unevaluated conditional with iterable to be evaluated if the
        conditional is true.

        :param DelayedEvaluator cond: conditional.
        :param list eval_list: empty list to store evaluators in the if branch.
        """
        self.conds.append((cond, branch))

    def eval(self):
        """
        Evaluate if-statements and all evaluable in its selected branch.
        """
        for cond, branch in self.conds:
            if cond.eval():
                return [e.eval() for e in branch]
        return []


class TransForTemplateMacro(Transformer):
    """
    Transformer for template macro.
    """
    def __init__(self, scope, known_symb):
        self.scope = scope
        self.known_symb = known_symb
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

    ##############
    # complement #
    ##############

    @v_args(inline=True)
    def comp(self, cond):
        return DelayedEvaluator('comp', (cond,))

    ##############
    # Arithmetic #
    ##############

    @v_args(inline=True)
    def neg(self, val):
        return DelayedEvaluator('neg', (val,))

    ##############
    # comparison #
    ##############

    @v_args(inline=True)
    def eq(self, lhs, rhs):
        return DelayedEvaluator('eq', (lhs, rhs))

    @v_args(inline=True)
    def neq(self, lhs, rhs):
        return DelayedEvaluator('neq', (lhs, rhs))

    @v_args(inline=True)
    def gt(self, lhs, rhs):
        return DelayedEvaluator('gt', (lhs, rhs))

    @v_args(inline=True)
    def gte(self, lhs, rhs):
        return DelayedEvaluator('gte', (lhs, rhs))

    @v_args(inline=True)
    def lt(self, lhs, rhs):
        return DelayedEvaluator('lt', (lhs, rhs))

    @v_args(inline=True)
    def lte(self, lhs, rhs):
        return DelayedEvaluator('lte', (lhs, rhs))

    ###########
    # boolean #
    ###########

    @v_args(inline=True)
    def op_and(self, cond1, cond2):
        return DelayedEvaluator('and', (cond1, cond2))

    @v_args(inline=True)
    def op_or(self, cond1, cond2):
        return DelayedEvaluator('or', (cond1, cond2))

    ####################
    # Variable loading #
    ####################

    @v_args(inline=True)
    def var(self, val):
        return DelayedEvaluator('val', (val, self.known_symb))

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
        *idx, iterable = args

        child_scope = Scope(parent=self.scope)
        exe = ForStmtEvaluator(idx, iterable, child_scope, self.known_symb)
        child_scope.evaluator = exe
        self.scope = child_scope

        return exe

    @v_args(inline=True)
    def endfor_stmt(self):
        if isinstance(self.scope.evaluator, ForStmtEvaluator):
            self.scope = self.scope.parent
            return False
        else:
            raise ValueError('Line {}: Unmatched "endfor" statement.'.format(
                self.lineno))

    @v_args(inline=True)
    def if_stmt(self, cond):
        child_scope = Scope(parent=self.scope)
        exe = IfStmtEvaluator(cond, child_scope)
        child_scope.evaluator = exe
        self.scope = child_scope

        return exe

    @v_args(inline=True)
    def elif_stmt(self, cond):
        exe = self.scope.evaluator
        if isinstance(exe, IfStmtEvaluator):
            child_scope = Scope(parent=self.scope.parent, evalulator=exe)
            exe.add_cond(cond, child_scope)
            self.scope = child_scope
            return False
        else:
            raise ValueError('Line {}: Unmatched "elif" statement.'.format(
                self.lineno))

    @v_args(inline=True)
    def else_stmt(self):
        exe = self.scope.evaluator
        if isinstance(exe, IfStmtEvaluator):
            child_scope = Scope(parent=self.scope.parent, evalulator=exe)
            exe.add_cond(DelayedEvaluator('true', ()), child_scope)
            self.scope = child_scope
            return False
        else:
            raise ValueError('Line {}: Unmatched "else" statement.'.format(
                self.lineno))

    @v_args(inline=True)
    def endif_stmt(self):
        if isinstance(self.scope.evaluator, IfStmtEvaluator):
            self.scope = self.scope.parent
            return False
        else:
            raise ValueError('Line {}: Unmatched "endif" statement.'.format(
                self.lineno))
