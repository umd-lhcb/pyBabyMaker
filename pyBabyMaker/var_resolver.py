#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Fri Jan 08, 2021 at 04:21 AM +0100

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
    rvalues: InitVar[List[str]] = []

    def __post_init__(self, rvalues):
        self.resolved = {}
        self.idx = 0
        self.deps = {v: find_all_vars(v) for v in rvalues}


class VariableResolver(object):
    def __init__(self, namespace, ordering):
        self.namespace = namespace
        self.ordering = ordering
        self.resolved_vars = []

    def resolve(self, scope, variables):
        # Since the resolution may fail, we shouldn't add temporarily resolve
        # variables to global list yet.
        resolved_local = []
        for name, var in variables.items():
            # Always resolve name in its own scope first
            pass

            # Now resolve in the namespace, with different scopes
            # ...and we follow a defined ordering

    @staticmethod
    def exhausted(var):
        return True if var.idx > len(var.deps) else False

    @staticmethod
    def sub(expr, vars_to_replace):
        """
        Substitute variables in an expression with the resolved variable names.
        """
        for orig, resolved in vars_to_replace.items():
            expr = re.sub(r'\b'+orig+r'\b', resolved, expr)
        return expr
