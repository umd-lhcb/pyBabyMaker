# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Sat Jul 06, 2019 at 06:33 PM -0400

from distutils.core import setup, Extension

import setuptools
import subprocess


###########
# Helpers #
###########

with open('README.md', 'r') as ld:
    long_description = ld.read()


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
    sources=["pyBabyMaker/io/TupleDump.cpp"],
    libraries=["RIO", "Tree"],
    library_dirs=[root_libdir],
    include_dirs=[root_incdir],
    extra_compile_args=extra_flags,
    language='c++',
)


#########
# Setup #
#########

setup(
    name='pyBabyMaker',
    version='0.1.0',
    author='Yipeng Sun',
    author_email='syp@umd.edu',
    description='Python babymaker (flat ntuple generation tool) library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yipengsun/pyBabyMaker',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License'
        'Operating System :: OS Independent'
    ],
    ext_modules=[TupleDumpExtension]
)
