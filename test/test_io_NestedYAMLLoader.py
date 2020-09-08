#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Wed Sep 09, 2020 at 04:53 AM +0800

import os
import pytest
import yaml

from pyBabyMaker.io.NestedYAMLLoader import NestedYAMLLoader

PWD = os.path.dirname(os.path.realpath(__file__))
PARDIR = os.path.join(PWD, os.pardir)
SAMPLE_YAML = os.path.join(PARDIR, 'samples', 'sample-babymaker.yml')


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
