# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Wed Sep 04, 2019 at 11:55 PM -0400

import setuptools
import subprocess
import sys
import re

from setuptools.command.test import test as TestCommand
from distutils.core import setup, Extension

from pyBabyMaker import version


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


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


########################
# Compile instructions #
########################

root_libdir = get_pipe_output('root-config --libdir')
root_incdir = get_pipe_output('root-config --incdir')

cxx_flags = get_pipe_output('root-config --cflags').split()

# Make sure to enable C++ 14 support
# extra_flags = cxx_flags
extra_flags = [re.sub(r'std=c\+\+11', 'std=c++14', f) for f in cxx_flags]

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
    version=version,
    author='Yipeng Sun',
    author_email='syp@umd.edu',
    description='Python babymaker (flat ntuple generation tool) library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yipengsun/pyBabyMaker',
    packages=setuptools.find_packages(),
    scripts=['bin/ntpdump', 'bin/babymaker'],
    include_package_data=True,
    install_requires=[
        'pyyaml'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent'
    ],
    ext_modules=[TupleDumpExtension],
    tests_require=['pytest'],
    test_suite="test",
    cmdclass={'test': PyTest}
)
