#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Sat Aug 31, 2019 at 03:52 PM -0400
"""
This module provides a YAML loader with ``!include`` directive so that other
YAML files can be included in the input YAML file.
"""

import yaml
import os


class NestedYAMLLoader(yaml.SafeLoader):
    """
    An extension to the standard ``SafeLoader`` to allow the inclusion of
    another YAML file.
    """
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super().__init__(stream)

    def include(self, node):
        """
        Load from another YAML file, the additional YAML file path must be
        relative to the original YAML file.

        .. warning::

            Tested to work with loading a ``list``, and **not** work with
            loading a ``dict``.
        """
        filename = os.path.join(self._root, self.construct_scalar(node))

        with open(filename, 'r') as f:
            return yaml.load(f, NestedYAMLLoader)


NestedYAMLLoader.add_constructor('!include', NestedYAMLLoader.include)
