#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Wed Jan 06, 2021 at 11:18 PM +0100

from dataclasses import dataclass, field

from pyBabyMaker.boolean.utils import find_all_vars


@dataclass
class Variable(object):
    """
    Store raw variable to be resolved.
    """
    type: str
    name: str
    deps: list(str) = field(
        default=[],
        default_factory=lambda x: [find_all_vars(i) for i in x])
