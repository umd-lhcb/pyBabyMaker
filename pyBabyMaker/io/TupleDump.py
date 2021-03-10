#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Wed Mar 10, 2021 at 11:34 PM +0100
"""
This module dumps all branch names and their types from all TTrees in a ntuple.
"""

import uproot


# This is super easy! And we get rid of ROOT dependency
class PyTupleDump:
    def __init__(self, ntp_path):
        self.ntp = uproot.open(ntp_path)

    def dump(self):
        return {self.tree_name(key): self.ntp[key].typenames()
                for key in self.ttree_only(self.ntp)}

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
