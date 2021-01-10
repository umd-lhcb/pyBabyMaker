#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Sun Jan 10, 2021 at 04:49 AM +0100

import re

from dataclasses import dataclass, InitVar
from typing import List

from pyBabyMaker.boolean.utils import find_all_vars


@dataclass
class Variable:
    """
    Store raw variable to be resolved.
    """
    name: str
    type: str = 'nil'
    rvalues: InitVar[List[str]] = ['']

    def __post_init__(self, rvalues):
        self.resolved = {}
        self.idx = 0
        self.deps = {v: find_all_vars(v) for v in rvalues}
        self.len = len(self.deps)

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

    def ok(self):
        """
        Return if current rvalue is fully resolved.
        """
        if len(self.resolved) == len(list(self.deps.values())[self.idx]):
            return True
        return False

    def sub(self):
        """
        Substitute variables in an expression with the resolved variable names.
        """
        expr = list(self.deps)[self.idx]
        for orig, resolved in self.resolved.items():
            expr = re.sub(r'\b'+orig+r'\b', resolved, expr)
        return expr


class VariableResolver(object):
    def __init__(self, namespace, ordering):
        self.namespace = namespace
        self.ordering = ordering

        self._resolved_vars = []

    def resolve_var(self, scope, var, ordering):
        load_seq = []
        num_of_scopes = len(ordering)
        deps = list(var.deps.values())[var.idx]

        for idx, other_scope in enumerate(ordering):
            for dep_var_name in deps:
                dep_var_name_resolved = other_scope+'_'+dep_var_name
                if dep_var_name_resolved in self._resolved_vars:
                    # If it's already loaded somewhere else, just use it
                    var.resolved[dep_var_name] = dep_var_name_resolved
                    break

                if dep_var_name in self.namespace[other_scope]:
                    dep_var = self.namespace[other_scope][dep_var_name]
                    if scope == other_scope and dep_var_name == var.name:
                        continue  # Don't do circular resolution

                    if idx+1 == num_of_scopes:
                        # We assume we can always load variables from the last
                        # scope
                        var.resolved[dep_var_name] = dep_var_name_resolved
                        self._resolved_vars.append(dep_var_name_resolved)
                        load_seq.append(self.format_resolved(
                            other_scope, dep_var))

                    else:
                        dep_load_status, dep_load_seq = self.resolve_var(
                            other_scope, dep_var, ordering[idx:])
                        if dep_load_status:
                            var.resolved[dep_var_name] = dep_var_name_resolved
                            load_seq += dep_load_seq
                        else:
                            break  # No point continue if a dep can't load

        if len(var.resolved) == len(deps):
            self._resolved_vars.append(scope+'_'+var.name)
            load_seq.append(self.format_resolved(scope, var))
            return True, load_seq  # Resolution successful

        # See if we tried all possible rvalues for this variable
        if var.next():  # this variable has more rvalues, try resolve it again
            return self.resolve_var(scope, var, ordering)

        return False, load_seq  # Failed to load

    @staticmethod
    def format_resolved(scope, var):
        return (scope, var)
