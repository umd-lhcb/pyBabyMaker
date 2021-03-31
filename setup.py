# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Wed Mar 31, 2021 at 10:53 PM +0200

import setuptools
import subprocess
import sys
import codecs
import os.path

from setuptools.command.test import test as TestCommand
from distutils.core import setup


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


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


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


#########
# Setup #
#########

setup(
    name='pyBabyMaker',
    version=get_version('pyBabyMaker/__init__.py'),
    author='Yipeng Sun',
    author_email='syp@umd.edu',
    description='Python babymaker (flat ntuple generation tool) library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/umd-lhcb/pyBabyMaker',
    packages=setuptools.find_packages(),
    scripts=['bin/ntpdump', 'bin/babymaker'],
    include_package_data=True,
    install_requires=[
        'pyyaml',
        'lark-parser',
        'uproot',
        'lz4'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent'
    ],
    tests_require=['pytest'],
    test_suite="test",
    cmdclass={'test': PyTest}
)
