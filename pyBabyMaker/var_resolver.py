#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Thu Jan 07, 2021 at 11:54 PM +0100

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
        default=[],
        default_factory=lambda x: {x: [find_all_vars(i) for i in x]})
    resolved: Dict[str, str] = []
    idx: int = 0


class VariableResolver(object):
    def __init__(self, ):
        pass

    @staticmethod
    def sub(expr, vars_to_replace):
        """
        Substitute variables in an expression with the resolved variable names.
        """
        for orig, resolved in vars_to_replace.items():
            expr = re.sub(r'\b'+orig+r'\b', resolved, expr)
        return expr
