# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD-clause
# Last Change: Sat Jul 06, 2019 at 12:34 AM -0400

# cython: language_level=3


from libcpp.string cimport string

from TupleDump cimport TupleDump


cdef class PyTupleDump:
    cdef TupleDump c_dump

    def __cinit__(self, string filename):
        self.c_dump.read(filename)

    def dump(self):
        return self.c_dump.dump()
