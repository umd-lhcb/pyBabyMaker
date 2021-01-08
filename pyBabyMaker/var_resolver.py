#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Fri Jan 08, 2021 at 04:48 AM +0100

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
        self.resolved_vars = []

    def resolve(self, scope, variables):
        for name, var in variables.items():
            # Always resolve name in its own scope first
            pass

            # Now resolve in the namespace, with different scopes
            # ...and we follow a defined ordering
