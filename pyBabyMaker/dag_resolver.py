#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Tue Aug 31, 2021 at 05:56 PM +0200
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
    literal: str = None

    @property
    def terminal(self):
        """
        Return a boolean indicating if the variable is terminal, which means
        that it is considered to be resolved directly
        """
        if not self.literal and not list(self):
            return True
        return False

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
            return '{} := {}'.format(self.name, '|'.join(self.rvals))
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
    literal: str = None
    parent: Node = None
    children: List[Node] = field(default_factory=list)

    @property
    def fake(self):
        """
        Return a boolean indicating if this Node represents a fake variable.

        A fake variable means that this is used to hold some expression to be
        resolved, e.g. a boolean expression in an if statement, but the
        expression doesn't need to be defined.
        """
        if not self.type and self.expr and not self.literal:
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
        if self.expr:
            val = self.expr
        elif self.literal:
            val = self.literal
        else:
            val = self.name  # For terminal variables

        for v in self.children:
            if v.literal:
                val = re.sub(r'\b'+v.name+r'\b', v.literal, val)
            else:
                val = re.sub(r'\b'+v.name+r'\b', v.fname, val)

        return val

    def __repr__(self):
        if self.literal:
            return '{} := {}'.format(self.name, self.literal)
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
    """
    Resolve a single variable traversing on scopes with a given ordering.
    """
    resolved_vars_now = []

    if var.terminal:
        node_root = Node(var.name, scope, var.type, parent=parent)
        DEBUG('Resolved raw variable: {}'.format(node_root))
        resolved_vars_now.append(node_root)
        if parent:
            parent.children.append(node_root)
        return True, node_root, resolved_vars_now

    if var.literal:
        node_root = Node(var.name, literal=var.literal, parent=parent)
        DEBUG('Resolved literal variable: {}'.format(node_root))
        # Don't add literal variables to resolved variable list
        if parent:
            parent.children.append(node_root)
        else:
            print('{}Literal variable {} as a root DAG node, something must be wrong here{}'.format(
                TC.RED, node_root, TC.END))
        return True, node_root, resolved_vars_now

    for rval, deps in var:  # Allow resolve variables with multiple rvalues
        is_resolved = True
        node_root = Node(var.name, scope, var.type, rval, parent=parent)

        if resolved_vars and node_root in resolved_vars:
            DEBUG('Already resolved: {}'.format(node_root))
            return is_resolved, node_root, resolved_vars_now

        resolved_vars_dep = []
        # Don't modify input!
        resolved_vars_copy = deepcopy(resolved_vars) if resolved_vars else []
        blocked_fnames = find_parent_fnames(node_root)

        for n in deps:
            for s in ordering:
                DEBUG('Try to resolve {} in {}...'.format(n, s))
                if n in scopes[s] and \
                        fname_formatter(s, n) not in blocked_fnames:
                    var_dep = scopes[s][n]
                    is_resolved, node_leaf, resolved_vars_add = resolve_var(
                        var_dep, s, scopes, ordering, node_root,
                        resolved_vars_copy)

                    if is_resolved:
                        node_root.children.append(node_leaf)  # append resolved to root
                        resolved_vars_dep += resolved_vars_add
                        resolved_vars_copy += resolved_vars_dep
                        break

                else:
                    DEBUG('Variable {} not in {}'.format(n, s))
                    is_resolved = False

        if is_resolved:
            resolved_vars_now += resolved_vars_dep
            resolved_vars_now.append(node_root)
            break

    return is_resolved, node_root, resolved_vars_now