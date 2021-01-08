#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Fri Jan 08, 2021 at 03:58 AM +0100

import re

from dataclasses import dataclass, field
from typing import Dict

from pyBabyMaker.boolean.utils import find_all_vars


@dataclass
class Variable(object):
    """
    Store raw variable to be resolved.
    """
    name: str
    type: str = 'nil'
    deps: Dict[str, list(str)] = field(
        default_factory=lambda x: {x: [find_all_vars(i) for i in x]})
    resolved: Dict[str, str] = {}
    idx: int = 0


class VariableResolver(object):
    def __init__(self, namespace, ordering):
        self.namespace = namespace
        self.ordering = ordering
        self.resolved_vars = []

    def resolve(self, scope, variables):
        # Since the resolution may fail, we shouldn't add temporarily resolve
        # variables to global list yet.
        resolved_local = []
        for name, var in variables:
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
