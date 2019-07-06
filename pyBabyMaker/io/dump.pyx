# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD-clause
# Last Change: Sat Jul 06, 2019 at 12:08 PM -0400

# cython: language_level=3

from libcpp.string cimport string

from TupleDump cimport TupleDump


cdef class PyTupleDump:
    cdef TupleDump c_dump

    def __cinit__(self, filename):
        self.c_dump.read(filename.encode('ascii'))

    def trees(self):
        raw_trees = self.c_dump.trees()
        return [t.decode('ascii') for t in raw_trees]
