#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Tue Aug 31, 2021 at 04:41 AM +0200
"""
This module provides general variable dependency resolution.

To be more technical, this is a Directed Acyclic Graph (DAG) resolver. I decided
traverse the DAG tree in a depth-first manner, so there's no laziness involved.
"""

from __future__ import annotations

import re
import logging

from dataclasses import dataclass, field
from typing import List, Dict
from copy import deepcopy
from itertools import product

from pyBabyMaker.boolean.utils import find_all_vars
from pyBabyMaker.base import TermColor as TC

DEBUG = logging.debug


##############
# Containers #
##############

def fname_formatter(scope, name):
    """
    Full name formatter.
    """
    return '{}_{}'.format(scope, name)


@dataclass
class Variable:
    """
    Store a raw variable to be resolved. Note that by design we allow multiple
    possible rvalues.

    This class is stateful only when used as an iterator.
    """
    name: str
    type: str = None
    rvals: List[str] = field(default_factory=list)
    literal: False

    def __iter__(self):
        self._idx = 0
        self._len = len(self.rvals)
        return self

    def __next__(self):
        if self._idx < self._len:
            idx = self._idx
            self._idx += 1
            return self.rvals[idx], find_all_vars(self.rvals[idx])
        raise StopIteration

    def __repr__(self):
        if self.literal:
            return '{} := {}'.format(self.name, self.literal)
        return '{} {} = {}'.format(self.type, self.name, '|'.join(self.rvals))


@dataclass
class Node:
    """
    Store a node in a DAG.
    """
    name: str
    scope: str = None
    type: str = None
    expr: str = None
    parent: Node = None
    children: List[Node] = field(default_factory=list)

    @property
    def is_literal(self):
        """
        Return a boolean indicating if this Node represents a literal variable.
        """
        if not self.children and self.expr:
            return True
        return False

    @property
    def is_fake(self):
        """
        Return a boolean indicating if this Node represents a fake variable.

        A fake variable means that this is used to hold some expression to be
        resolved, e.g. a boolean expression in an if statement, but the
        expression doesn't need to be defined.
        """
        if not self.type:
            return True
        return False

    @property
    def fname(self):
        """
        Return the fullname of the variable, including a scope prefix.
        """
        return fname_formatter(self.scope, self.name)

    @property
    def rval(self):
        """
        Substitute variables in resolved rvalue with the resolved variable
        names.

        Suppose ``a -> calc_a``, and ``b -> rename_b``, then a rvalue of
        ``a+b -> calc_a+rename_b``.
        """
        val = self.expr

        for v in self.children:
            if v.is_literal:
                val = re.sub(r'\b'+v.name+r'\b', v.expr, val)
            else:
                val = re.sub(r'\b'+v.name+r'\b', v.fname, val)

        return val

    def __repr__(self):
        if self.is_literal:
            return '{} := {}'.format(self.name, self.expr)
        return '{} {}.{} = {}'.format(
            self.type, self.scope, self.name, self.rval)

    def __eq__(self, other):
        if type(self) == type(other) and \
                self.name == other.name and self.scope == other.scope and \
                self.type == other.type and self.expr == other.expr:
            return True
        return False


################################
# Variable resolver with a DAG #
################################

def find_parent_fnames(var):
    """
    Find full names of parents, recursively.

    These names will be forbidden in the subsequent resolution to make sure
    there's no back branch in the constructed DAG.
    """
    names = []
    if var.parent:
        names.append(var.parent.fname)
        names += find_parent_fnames(var.parent)
    return names


def resolve_var(var, scope, scopes, ordering, parent=None, resolved_vars=None):
    # Don't mutate inputs!
    resolved_vars = [] if not resolved_vars else deepcopy(resolved_vars)
    blocked_fnames = None
    is_resolved = False

    for rval, deps in var:
        node_root = Node(var.name, scope, var.type, rval, parent=parent)
        resolved_vars_dep = []
        # First store all resolved parent names ONLY ONCE
        if blocked_fnames is not None:
            blocked_fnames = find_parent_fnames(node_root)

        dep_ok = True
        for s, n in product(deps, ordering):
            if n in scopes[s] and fname_formatter(s, n) not in blocked_fnames:
                var_dep = scopes[s][n]
                dep_ok, node_leaf, resolved_vars_add = resolve_var(
                    var_dep, s, scopes, ordering, node_root, resolved_vars)

                if not dep_ok:
                    break

                node_root.children.append(node_leaf)
                resolved_vars_dep += resolved_vars_add

        if dep_ok:
            is_resolved = True
            resolved_vars += resolved_vars_dep
            break

    return is_resolved, node_root, resolved_vars
