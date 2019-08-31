#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Sat Aug 31, 2019 at 01:00 AM -0400

import os
import pytest
import yaml

from pyBabyMaker.io.NestedYAMLLoader import NestedYAMLLoader

PWD = os.path.dirname(os.path.realpath(__file__))
SAMPLE_YAML = os.path.join(PWD, 'sample-ntuple_process.yml')
SAMPLE_YAML_SUBSECTION = os.path.join(PWD,
                                      'sample-ntuple_process-subsection.yml')


@pytest.fixture
def default_Loader():
    with open(SAMPLE_YAML, 'r') as f:
        return yaml.load(f, NestedYAMLLoader)


def test_NestedYAMLLoader_values(default_Loader):
    result = default_Loader
    assert result['YetYetAnotherTuple']['force_lowercase']
