# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Sat Jul 06, 2019 at 05:22 PM -0400

from distutils.core import setup, Extension

import subprocess


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
extra_flags = cxx_flags

TupleDumpExtension = Extension(
    name="pyBabyMaker.io.TupleDump",
    sources=["pyBabyMaker/io/dump.cpp"],
    libraries=["RIO", "Tree"],
    library_dirs=[root_libdir],
    include_dirs=[root_incdir],
    extra_compile_args=extra_flags,
    language='c++',
)

setup(ext_modules=[TupleDumpExtension])
