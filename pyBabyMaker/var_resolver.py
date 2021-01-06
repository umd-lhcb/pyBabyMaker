#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Wed Jan 06, 2021 at 11:32 PM +0100

from dataclasses import dataclass, field
from typing import Dict

from pyBabyMaker.boolean.utils import find_all_vars


@dataclass
class Variable(object):
    """
    Store raw variable to be resolved.
    """
    type: str
    name: str
    deps: Dict[str, list(str)] = field(
        default=[],
        default_factory=lambda x: {x: [find_all_vars(i) for i in x]})
    resolved: list(str) = []
    idx: int = 0
