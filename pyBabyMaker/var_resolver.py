#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Tue Aug 10, 2021 at 03:57 PM +0200
"""
This module provides general variable dependency resolution.

I (Yipeng) commit a lot of sins in this module by recording states all around
the places. This should be fixed by a rewrite but we don't have time now.
"""

import re
import logging

from dataclasses import dataclass, field
from typing import List, Dict

from pyBabyMaker.boolean.utils import find_all_vars
from pyBabyMaker.base import TermColor as TC
from pyBabyMaker.base import UniqueList

DEBUG = logging.debug


@dataclass
class Variable:
    """
    Store raw variable to be resolved.
    """
    name: str
    type: str = 'nil'
    rvalues: List[str] = field(default_factory=lambda: [''])
    deps: Dict[str, List[str]] = field(init=False)
    literal: str = None

    def __post_init__(self):
        self.resolved = {}
        self.idx = 0
        self.deps = {rv: find_all_vars(rv) for rv in self.rvalues}
        self.len = len(self.deps)

    def __repr__(self):
        if self.literal is not None:
            return '{} := {}'.format(self.name, self.literal)
        return '{} {} = {}'.format(self.type, self.name, '|'.join(self.rvalues))

    def next(self):
        """
        Prepare to resolve next possible rvalues and its dependencies, if
        there's one. Return ``True`` in this case.

        Otherwise return ``False``.
        """
        if self.idx+1 >= self.len:
            return False
        self.idx += 1
        self.resolved = {}
        return True

    def reset(self):
        """
        Reset the variable to its initial condition for possible resolution
        later.
        """
        self.__post_init__()

    @property
    def ok(self):
        """
        Return if current rvalue is fully resolved.
        """
        if self.literal is not None or len(self.resolved) == \
                len(list(self.deps.values())[self.idx]):
            return True
        return False

    @property
    def rval(self):
        """
        Substitute variables in resolved rvalue with the resolved variable
        names.

        Suppose ``a -> calc_a``, and ``b -> rename_b``, then a rvalue of
        ``a+b -> calc_a+rename_b``.
        """
        if self.literal is not None:
            return self.literal

        expr = list(self.deps)[self.idx]
        for orig, resolved in self.resolved.items():
            expr = re.sub(r'\b'+orig+r'\b', resolved, expr)
        return expr


class VariableResolver(object):
    """
    General variable resolver.
    """
    def __init__(self, namespace, skip_names=None):
        self.namespace = namespace
        self._resolved_names = []
        self.skip_names = [] if skip_names is None else skip_names

    def resolve_scope(self, scope, ordering=None):
        """
        Resolve all variables in a single scope.

        **Note**: If ``ordering`` is not supplied, it will use an ordering that
        passes all known scopes with ``scope`` being first and ``raw`` last.
        """
        if scope not in self.namespace:
            print('{}Unknown scope: {}.{}'.format(TC.YELLOW, scope, TC.END))
            return [], []

        ordering = [scope] + [o for o in self.namespace.keys()
                              if o != 'raw' and o != scope] + ['raw'] \
            if ordering is None else ordering
        DEBUG('Ordering for walking through namespaces: {}.'.format(
            ', '.join(ordering)))
        return self.resolve_vars_in_scope(
            scope, self.namespace[scope].values(), ordering)

    def resolve_vars_in_scope(self, scope, variables, ordering=['raw']):
        """
        Resolve multiple variables in namespaces following an ordering.
        """
        load_seq = []
        unresolved = []

        for var in variables:
            DEBUG('Current scope is: {}'.format(scope))
            status, var_load_seq, var_known_name = self.resolve_var(
                scope, var, ordering)
            if status:
                load_seq += var_load_seq
                self._resolved_names += var_known_name
            else:
                DEBUG('Not resolvable: {}'.format(var))
                unresolved.append(var)
                # Reset resolved variables in this round
                self.reset_resolved_vars(var_load_seq)

        return load_seq, unresolved

    def reset_resolved_vars(self, load_seq):
        """
        Reset resolved variables in ``load_seq`` so they can be resolved again
        instead of falsely considered to be already resolved.
        """
        for data in load_seq:
            scope, var_name = self.unpack_resolved(data)
            try:
                DEBUG('Resetting {}.{}...'.format(scope, var_name))
                self.namespace[scope][var_name].reset()
            except:
                DEBUG('Failed to reset {}.{}, proceed anyway...'.format(
                    scope, var_name))

    def resolve_var(self, scope, var, ordering=['raw'], known_names=None):
        """
        Resolve a single variable in namespaces following an ordering.
        """
        load_seq = UniqueList()
        known_names = UniqueList() if known_names is None else known_names
        var_key = (scope, var.name)
        DEBUG('Start resolving: {}.{}'.format(scope, var.name))

        if var_key in self._resolved_names or var_key in known_names:
            DEBUG('Variable {}.{} already resolved. Return right away.'.format(
                scope, var.name))
            return True, load_seq, known_names

        for idx, other_scope in enumerate(ordering):
            if var.ok:
                DEBUG('All dependencies of variable {} already resolved, break.'.format(
                    var.name))
                break

            deps = [i for i in list(var.deps.values())[var.idx]
                    if i not in var.resolved and
                    (other_scope != scope or i != var.name)]
            DEBUG('Resolving dependencies ({}) in {} of variable {}.{}.'.format(
                ','.join(deps), other_scope, scope, var.name))
            # Here we already remove self-referential cases in the same scope

            for dep_var_name in deps:
                dep_var_name_resolved = other_scope+'_'+dep_var_name
                dep_var_key = (other_scope, dep_var_name)

                # NOTE: Handling of skipped names
                #       They should only be part of the rvalues
                if dep_var_name in self.skip_names:
                    DEBUG('Skipping name {}...'.format(var.name))
                    var.resolved[dep_var_name] = dep_var_name

                elif dep_var_name in self.namespace[other_scope]:
                    dep_var = self.namespace[other_scope][dep_var_name]

                    # Handle literal variables
                    if dep_var.literal is not None:
                        DEBUG('Handle literal variable {}...'.format(var.name))
                        var.resolved[dep_var_name] = dep_var.literal
                        continue

                    # The last scope should only contain variables that don't
                    # need further resolution.
                    if idx+1 == len(ordering):
                        var.resolved[dep_var_name] = dep_var_name_resolved
                        if dep_var_key in self._resolved_names or \
                                dep_var_key in known_names:
                            DEBUG('Dep variable {}.{} already resolved.'.format(
                                scope, dep_var.name))
                            continue

                        DEBUG('Resolved dep {}.{} in terminal scope {}'.format(
                            other_scope, dep_var_name, other_scope))
                        known_names.append(dep_var_key)
                        load_seq.append(self.format_resolved(
                            other_scope, dep_var))

                    else:
                        DEBUG('Try to resolve dep {}.{}.'.format(
                            other_scope, dep_var_name))
                        dep_load_status, dep_load_seq, dep_known_names = \
                            self.resolve_var(other_scope, dep_var,
                                             ordering[idx:], known_names)
                        # Always update these to keep track of all variables we
                        # have accessed
                        load_seq += dep_load_seq
                        known_names += dep_known_names

                        if dep_load_status:
                            DEBUG('Resolved dep {}.{}.'.format(
                                other_scope, dep_var_name))
                            var.resolved[dep_var_name] = dep_var_name_resolved

        if var.ok:
            DEBUG('Fully resolved: {}.{}.'.format(scope, var.name))
            known_names.append(var_key)
            load_seq.append(self.format_resolved(scope, var))
            return True, load_seq, known_names  # Resolution successful

        if var.next():
            DEBUG('Trying alternative rvalues for variable {}.{}'.format(
                scope, var.name))
            # Reset variables used in this round only
            self.reset_resolved_vars(load_seq)
            return self.resolve_var(scope, var, ordering)

        return False, load_seq, known_names  # Failed to load

    @staticmethod
    def format_resolved(scope, var):
        """
        Format resolved variable.
        """
        return scope, var

    @staticmethod
    def unpack_resolved(data):
        """
        Unpack resolved variable to (scope, original variable name) tuple.
        """
        scope, var = data
        return scope, var.name
