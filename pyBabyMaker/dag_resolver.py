#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Tue Aug 31, 2021 at 02:18 AM +0200
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

from pyBabyMaker.boolean.utils import find_all_vars
from pyBabyMaker.base import TermColor as TC

DEBUG = logging.debug


############
# DAG Tree #
############

@dataclass
class Node:
    """
    Store a node in a DAG.
    """
    name: str
    scope: str = None
    type: str = None
    expr: str = None
    mother: Node = None
    children: List[Node] = field(default_factory=list)

    @property
    def is_literal(self):
        """
        Return a boolean indicating if this Node represents a literal variable.
        """
        if not self.children and self.expr:
            return True
        return False

    @property
    def fname(self):
        """
        Return the fullname of the variable, including a scope prefix.
        """
        return '{}_{}'.format(self.scope, self.name)

    @property
    def rval(self):
        """
        Substitute variables in resolved rvalue with the resolved variable
        names.

        Suppose ``a -> calc_a``, and ``b -> rename_b``, then a rvalue of
        ``a+b -> calc_a+rename_b``.
        """
        val = self.expr

        for v in self.children:
            if v.is_literal:
                val = re.sub(r'\b'+v.name+r'\b', v.expr, val)
            else:
                val = re.sub(r'\b'+v.name+r'\b', v.fname, val)

        return val

    def __repr__(self):
        if self.is_literal:
            return '{} := {}'.format(self.name, self.expr)

        return '{} {}.{} = {}'.format(
            self.type, self.scope, self.name, self.rval)

    def __eq__(self, other):
        try:
            if self.name == other.name and self.scope == other.scope and \
                    self.type == other.type and self.expr == other.expr:
                return True
            return False
        except AttributeError:
            return False


#####################
# Variable resolver #
#####################

@dataclass
class InputVariable:
    """
    Store a raw variable to be resolved. Note that by design we allow multiple
    possible rvalues.

    This class is stateful only when used as an iterator.
    """
    name: str
    type: str = 'nil'
    rvals: List[str] = field(default_factory=list)
    literal: str = None

    def __iter__(self):
        self.idx = 0
        self.len = len(self.rvals)
        return self

    def __next__(self):
        if self.idx < self.len:
            self.idx += 1
            return find_all_vars(self.rvals[self.idx - 1])
        raise StopIteration

    def __repr__(self):
        if self.literal is not None:
            return '{} := {}'.format(self.name, self.literal)
        return '{} {} = {}'.format(self.type, self.name, '|'.join(self.rvals))
