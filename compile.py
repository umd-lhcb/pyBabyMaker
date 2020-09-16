# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Thu Sep 17, 2020 at 01:45 AM +0800

import subprocess
import re

from distutils.core import setup, Extension
from Cython.Build import cythonize


###########
# Helpers #
###########

def get_pipe_output(cmd):
    cmd_splitted = cmd.split(' ')
    proc = subprocess.Popen(cmd_splitted, stdout=subprocess.PIPE)
    result = proc.stdout.read().decode('utf-8')
    return result.strip('\n')


########################
# Compile instructions #
########################

root_libdir = get_pipe_output('root-config --libdir')
root_incdir = get_pipe_output('root-config --incdir')

cxx_flags = get_pipe_output('root-config --cflags').split()

# Make sure to enable C++ 14 support
extra_flags = [re.sub(r'std=c\+\+11', 'std=c++14', f) for f in cxx_flags]

TupleDumpExtension = Extension(
    name="pyBabyMaker.io.TupleDump",
    sources=["pyBabyMaker/io/TupleDump.pyx"],
    libraries=["RIO", "Tree"],
    library_dirs=[root_libdir],
    include_dirs=[root_incdir],
    extra_compile_args=extra_flags,
    language='c++',
)

setup(ext_modules=cythonize([TupleDumpExtension]))
