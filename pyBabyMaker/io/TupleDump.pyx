# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD-clause
# Last Change: Thu Sep 17, 2020 at 01:43 AM +0800

# cython: language_level=3

from libcpp.string cimport string

from .TupleDump cimport TupleDump


cdef class PyTupleDump:
    cdef TupleDump c_dump

    def __cinit__(self, filename):
        self.c_dump.read(filename.encode('ascii'))

    def dump(self):
        result = {}

        for t in self.trees():
            result[t] = {}
            for b in self.branches(t):
                result[t][b] = self.datatype(t, b)

        return result

    def trees(self):
        raw_trees = self.c_dump.trees()
        return [t.decode('ascii') for t in raw_trees]

    def branches(self, tree):
        raw_branches = self.c_dump.branches(
            tree.encode('ascii'))
        return [t.decode('ascii') for t in raw_branches]

    def datatype(self, tree, branch):
        raw_datatype = self.c_dump.datatype(
            tree.encode('ascii'), branch.encode('ascii'))
        return raw_datatype.decode('ascii')
