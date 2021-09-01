#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Wed Sep 01, 2021 at 05:47 PM +0200
"""
This module provides general variable dependency resolution.

To be more technical, this is a Directed Acyclic Graph (DAG) resolver. I decided
traverse the DAG tree in a depth-first manner, so there's no laziness involved.
"""

from __future__ import annotations

import re
import logging

from dataclasses import dataclass, field
from typing import List

from pyBabyMaker.boolean.utils import find_all_vars
from pyBabyMaker.base import TermColor as TC
from pyBabyMaker.base import UniqueList

DEBUG = logging.debug


##############
# Containers #
##############

def fname_formatter(scope, name):
    """
    Full name formatter.
    """
    return '{}_{}'.format(scope, name)


def propagate_io_attr(var, node):
    """
    Make sure the 'input' and 'output' attrs are the same between `var` and
    `node`.
    """


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
    input: bool = False
    output: bool = True

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
    children: List[Node] = field(default_factory=UniqueList)
    input: bool = False
    output: bool = True

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
        return '{} {}_{} = {}'.format(
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
    names = [var.fname]  # No self-referential
    if var.parent:
        names.append(var.parent.fname)
        names += find_parent_fnames(var.parent)
    return names


def resolve_var(var, scope, scopes, ordering,
                parent=None, resolved_vars=None, resolved_vars_mutable=None,
                skip_names=None, postprocess=propagate_io_attr):
    """
    Resolve a single variable traversing on scopes with a given ordering.

    This is the main function that is responsible for DAG node resolution. Read
    this with care!
    """
    resolved_vars_now = []
    skip_names = [] if skip_names is None else skip_names

    if var.terminal:
        node_root = Node(var.name, scope, var.type, parent=parent)
        postprocess(var, node_root)
        DEBUG('Resolved raw variable: {}'.format(node_root))
        if parent:
            parent.children.append(node_root)
        return True, node_root, [node_root]

    if var.literal:
        node_root = Node(var.name, literal=var.literal, parent=parent)
        postprocess(var, node_root)
        DEBUG('Resolved literal variable: {}'.format(node_root))
        # Don't add literal variables to resolved variable list
        if parent:
            parent.children.append(node_root)
        else:
            print('{}Literal variable {} as a root DAG node, something must be wrong here{}'.format(
                TC.RED, node_root, TC.END))
        return True, node_root, []

    for rval, deps in var:  # Allow resolve variables with multiple rvalues
        resolved_vars_mutable = [] if resolved_vars_mutable is None else \
            resolved_vars_mutable  # This is flushed for each rvalue
        node_root = Node(var.name, scope, var.type, rval, parent=parent)
        postprocess(var, node_root)
        DEBUG('Try to resolve dependencies of {}...'.format(node_root))

        if resolved_vars and node_root in resolved_vars:
            DEBUG('Already resolved: {}'.format(node_root))
            return True, resolved_vars[resolved_vars.index(node_root)], []

        if node_root in resolved_vars_mutable:
            DEBUG('Already resolved: {}'.format(node_root))
            return True, resolved_vars_mutable[
                resolved_vars_mutable.index(node_root)], []

        resolved_vars_dep = []
        blocked_fnames = find_parent_fnames(node_root)

        dep_resolved = {n: False for n in deps}
        for n in deps:
            for s in ordering:
                DEBUG('Try to resolve dependency {} in {}...'.format(n, s))
                if n in skip_names:
                    DEBUG('Skipping {}...'.format(n))
                    dep_resolved[n] = True
                    break

                elif n in scopes[s] and \
                        fname_formatter(s, n) not in blocked_fnames:
                    var_dep = scopes[s][n]
                    is_resolved, node_leaf, resolved_vars_add = resolve_var(
                        var_dep, s, scopes, ordering, node_root,
                        resolved_vars, resolved_vars_mutable, skip_names,
                        postprocess)

                    if is_resolved:
                        DEBUG('Resolved dependency: {}'.format(node_leaf))
                        node_root.children.append(node_leaf)  # append resolved to root
                        resolved_vars_dep += resolved_vars_add
                        resolved_vars_mutable += resolved_vars_add
                        dep_resolved[n] = True
                        break

                else:
                    DEBUG('Dependency {} not in {}'.format(n, s))

        var_resolved = not (False in list(dep_resolved.values()))
        if var_resolved:
            resolved_vars_now += resolved_vars_dep
            resolved_vars_now.append(node_root)
            DEBUG('Resolved: {}'.format(node_root))
            break

        DEBUG('Reset resolved_vars_mutable...')
        resolved_vars_mutable = None  # Reset since the resolution failed

    return var_resolved, node_root, resolved_vars_now


def resolve_vars_in_scope(vars, scope, scopes, ordering,
                          resolved_vars=None, **kwargs):
    """
    Resolve specified variables in scopes.
    """
    resolved = [] if resolved_vars is None else resolved_vars
    failed = []

    for v in vars:
        is_resolved, node, resolved_append = resolve_var(
            v, scope, scopes, ordering, resolved_vars=resolved, **kwargs)

        if is_resolved:
            resolved += resolved_append
        else:
            failed.append(node)

    return resolved, failed


def resolve_scope(scope, scopes, ordering, **kwargs):
    """
    Resolve all variables in a scope
    """
    if scope in scopes:
        return resolve_vars_in_scope(
            scopes[scope].values(), scope, scopes, ordering, **kwargs)
    return [], []
