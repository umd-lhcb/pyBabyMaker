#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Fri Aug 30, 2019 at 09:12 PM -0400
"""
This module provides a YAML loader with '!include' directive so that other YAML
files can be included in the input YAML file.
"""

import yaml
import os


class NestedYAMLLoader(yaml.SafeLoader):
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super().__init__(stream)

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))

        with open(filename, 'r') as f:
            return yaml.load(f, NestedYAMLLoader)


NestedYAMLLoader.add_constructor('!include', NestedYAMLLoader.include)
