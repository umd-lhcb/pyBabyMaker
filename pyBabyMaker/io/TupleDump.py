#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Wed Mar 10, 2021 at 10:50 PM +0100
"""
This module dumps all branch names and their types from all TTrees in a ntuple.
"""

import uproot


# This is super easy! And we get rid of ROOT dependency
class PyTupleDump:
    def __init__(self, ntp_path):
        self.ntp = uproot.open(ntp_path)

    def dump(self):
        return {tree: self.ntp[tree].typenames() for tree in self.ntp
                if self.classname(self.ntp[tree]) == 'TTree'}

    @staticmethod
    def classname(obj):
        try:
            return obj.classname
        except AttributeError:
            return type(obj).__name__
