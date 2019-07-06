# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Sat Jul 06, 2019 at 05:21 PM -0400

# cython: language_level=3

from libcpp.vector cimport vector
from libcpp.string cimport string

cdef extern from "TupleDump_unwrapped/TupleDump.cpp":
    pass

cdef extern from "TupleDump_unwrapped/TupleDump.h" namespace "pyBabyMaker":
    cdef cppclass TupleDump:
        TupleDump() except +
        void read(string filename)
        vector[string] trees()
        vector[string] branches(string tree)
        string datatype(string tree, string branch)
