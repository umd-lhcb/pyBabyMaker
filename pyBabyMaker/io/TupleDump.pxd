# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Sat Jul 06, 2019 at 02:58 AM -0400

# cython: language_level=3

from libcpp.vector cimport vector
from libcpp.string cimport string

cdef extern from "TupleDump.cpp":
    pass

cdef extern from "TupleDump.h" namespace "pyBabyMaker":
    cdef cppclass TupleDump:
        TupleDump() except +
        vector[string] dump()
        void read(string filename)
