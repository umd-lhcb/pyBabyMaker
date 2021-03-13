#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Sat Mar 13, 2021 at 04:37 PM +0100
"""
This module dumps all branch names and their types from all TTrees in a ntuple.
"""

import uproot


# This is super easy! And we get rid of ROOT dependency
class PyTupleDump:
    def __init__(self, ntp_path):
        self.ntp = uproot.open(ntp_path)

    def dump(self):
        return {self.tree_name(tree):
                {k: self.type_hint(v)
                 for k, v in self.ntp[tree].typenames().items()}
                for tree in self.ttree_only(self.ntp)}

    @classmethod
    def ttree_only(cls, ntp, keey_highest_cycle_only=True):
        result = []

        oldkey = None
        for key in ntp:
            if cls.classname(ntp[key]) == 'TTree':
                if oldkey and (cls.tree_name(oldkey) != cls.tree_name(key) or
                               not keey_highest_cycle_only):
                    result.append(oldkey)
                oldkey = key
        result.append(oldkey)

        return result

    @staticmethod
    def classname(obj):
        try:
            return obj.classname
        except AttributeError:
            return obj.__class__.__name__

    @staticmethod
    def tree_name(key):
        return key.split(';')[0]

    @staticmethod
    def type_hint(typename):
        hints = {
            'uint64_t': 'ULong64_t',
            'uint32_t': 'UInt_t'
        }
        if typename in hints:
            return hints[typename]
        return typename
