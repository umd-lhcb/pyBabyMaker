#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Sun Oct 04, 2020 at 12:18 AM +0800

import pytest
import os

from unittest.mock import patch

from pyBabyMaker.base import UniqueList
from pyBabyMaker.base import BaseMaker
from pyBabyMaker.base import update_config

PWD = os.path.dirname(os.path.realpath(__file__))
PARDIR = os.path.join(PWD, os.pardir)
SAMPLE_YAML = os.path.join(PARDIR, 'samples', 'sample-babymaker.yml')
SAMPLE_ROOT = os.path.join(PARDIR, 'samples', 'sample.root')


###########
# Helpers #
###########

def test_BabyConfigParser_update_config():
    config = {'a': 1, 'b': 2, 'e': [1, 2]}
    update = {'a': 2, 'c': 3, 'e': [3]}
    result = update_config(config, update)

    assert result['a'] == 2
    assert result['b'] == 2
    assert result['c'] == 3
    assert result['e'] == [1, 2, 3]


def test_BabyConfigParser_update_config_merge_dict():
    config = {'a': 1, 'b': 2, 'e': {1: 2, 3: 4}}
    update = {'a': 2, 'c': 3, 'e': {1: 3, 2: 4}}
    result = update_config(config, update)

    assert result['a'] == 2
    assert result['b'] == 2
    assert result['c'] == 3
    assert result['e'] == {1: 3, 2: 4, 3: 4}


def test_BabyConfigParser_update_config_no_merge():
    config = {'a': 1, 'b': 2, 'e': [1, 2]}
    update = {'a': 2, 'c': 3, 'e': [3]}
    result = update_config(config, update, merge=False)

    assert result['a'] == 2
    assert result['b'] == 2
    assert result['c'] == 3
    assert result['e'] == [3]


##################
# Data structure #
##################

# UniqueList ###################################################################

@pytest.fixture
def default_UniqueList():
    return UniqueList([1, 2, 3, 1])


def test_UniqueList__init__normal():
    test_list = UniqueList()
    assert test_list == []


def test_UniqueList__init__duplicate(default_UniqueList):
    assert default_UniqueList == [1, 2, 3]


def test_UniqueList__init__exception():
    test_list = UniqueList([1, 2, 3, 4])
    assert test_list == [1, 2, 3, 4]


def test_UniqueList__add__normal(default_UniqueList):
    test_list = default_UniqueList + [7]
    assert test_list == [1, 2, 3, 7]


def test_UniqueList__add__duplicate(default_UniqueList):
    test_list = default_UniqueList + [7, 1, 2]
    assert test_list == [1, 2, 3, 7]


def test_UniqueList__iadd__normal(default_UniqueList):
    default_UniqueList += [7]
    assert default_UniqueList == [1, 2, 3, 7]


def test_UniqueList__iadd__duplicate(default_UniqueList):
    default_UniqueList += [7, 1, 2]
    assert default_UniqueList == [1, 2, 3, 7]


def test_UniqueList_append_normal(default_UniqueList):
    default_UniqueList.append(4)
    assert default_UniqueList == [1, 2, 3, 4]


def test_UniqueList_append_duplicate(default_UniqueList):
    default_UniqueList.append(1)
    assert default_UniqueList == [1, 2, 3]


def test_UniqueList_insert_normal(default_UniqueList):
    default_UniqueList.insert(0, 0)
    assert default_UniqueList == [0, 1, 2, 3]


def test_UniqueList_insert_duplicate(default_UniqueList):
    default_UniqueList.insert(0, 1)
    assert default_UniqueList == [1, 2, 3]


##############
# Base maker #
##############

class SimpleMaker(BaseMaker):
    def directive_gen(self, filename):
        pass

    def gen(self, filename):
        pass


@pytest.fixture
def default_SimpleMaker():
    return SimpleMaker()


def test_SimpleMaker_read(default_SimpleMaker):
    result = default_SimpleMaker.read(SAMPLE_YAML)
    assert result['output']['YetAnotherTuple']['drop'] == [
        'Y_OWNPV_COV_', 'Y_OWNPV_P.*']


def test_SimpleMaker_dump_scalar(default_SimpleMaker):
    result = default_SimpleMaker.dump(SAMPLE_ROOT)
    assert result['TupleB0/DecayTree']['CaloBremChi2'] == 'Float_t'


@pytest.mark.xfail(reason="Don't know how to detect vector with ROOT C++ code.")
def test_SimpleMaker_dump_vector(default_SimpleMaker):
    result = default_SimpleMaker.dump(SAMPLE_ROOT)
    assert result['TupleB0/DecayTree']['Y_OWNPV_COV_'] == 'vector<Float_t>'


def test_SimpleMaker_reformat(default_SimpleMaker):
    with patch('pyBabyMaker.base.which', return_value=True), \
            patch('subprocess.Popen') as m:
        default_SimpleMaker.reformat('cpp_filename')
        m.assert_called_once_with(['clang-format', '-i', 'cpp_filename'])
