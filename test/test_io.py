#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Thu Mar 11, 2021 at 12:30 AM +0100

import os
import pytest
import yaml

from pyBabyMaker.io.NestedYAMLLoader import NestedYAMLLoader
from pyBabyMaker.io.TupleDump import PyTupleDump

PWD = os.path.dirname(os.path.realpath(__file__))
PARDIR = os.path.join(PWD, os.pardir)
SAMPLE_YAML = os.path.join(PARDIR, 'samples', 'sample-babymaker.yml')
SAMPLE_NTP = os.path.join(PARDIR, 'samples', 'sample.root')


@pytest.fixture
def default_Loader():
    with open(SAMPLE_YAML, 'r') as f:
        return yaml.load(f, NestedYAMLLoader)


def test_NestedYAMLLoader_values(default_Loader):
    result = default_Loader
    assert result['rename'] == {
        k: k.lower() for k in ['Y_PT', 'Y_PX', 'Y_PY', 'Y_PZ', 'b0_PE']}


def test_NestedYAMLLoader_subfile_values(default_Loader):
    result = default_Loader
    assert result['output']['YetAnotherTuple']['drop'] == [
        'Y_OWNPV_COV_', 'Y_OWNPV_P.*']


def test_PyTupleDump():
    result = PyTupleDump(SAMPLE_NTP).dump()

    assert result['TupleB0/DecayTree']['CaloPrsE'] == 'float'
    assert result['TupleB0WSPi/DecayTree']['D0_ENDVERTEX_COV_'] == 'float[3][3]'
