#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Sat Sep 05, 2020 at 12:35 AM +0800

import pytest
import os
import yaml

from pyBabyMaker.babymaker import BabyConfigParser
from pyBabyMaker.base import Variable, UniqueList

from pyBabyMaker.io.NestedYAMLLoader import NestedYAMLLoader
from pyBabyMaker.io.TupleDump import PyTupleDump

PWD = os.path.dirname(os.path.realpath(__file__))
PARDIR = os.path.join(PWD, os.pardir)
SAMPLE_YAML = os.path.join(PARDIR, 'samples', 'sample-babymaker.yml')
SAMPLE_ROOT = os.path.join(PARDIR, 'samples', 'sample.root')


@pytest.fixture
def load_files():
    with open(SAMPLE_YAML) as f:
        parsed_config = yaml.load(f, NestedYAMLLoader)
    dumped_ntuple = PyTupleDump(SAMPLE_ROOT).dump()
    return (parsed_config, dumped_ntuple)


@pytest.fixture
def default_BabyConfigParser():
    return BabyConfigParser(None, None)


@pytest.fixture
def realistic_BabyConfigParser(load_files):
    return BabyConfigParser(*load_files)


##########################
# Parse YAML config file #
##########################

def test_BabyConfigParser_parse_ATuple(realistic_BabyConfigParser):
    directive = realistic_BabyConfigParser.parse()

    assert directive['trees']['ATuple']['input_tree'] == \
        'TupleB0/DecayTree'
    assert directive['trees']['ATuple']['input_branches'] == [
        Variable('Double_t', 'Y_PT'),
        Variable('Double_t', 'Y_PE'),
        Variable('Double_t', 'Y_PX'),
        Variable('Double_t', 'Y_PY'),
        Variable('Double_t', 'Y_PZ'),
        Variable('Double_t', 'D0_P'),
    ]
    assert directive['trees']['ATuple']['output_branches'] == [
        Variable('Double_t', 'y_pt', 'Y_PT'),
        Variable('Double_t', 'Y_PE', 'Y_PE'),
        Variable('Double_t', 'y_px', 'Y_PX'),
        Variable('Double_t', 'y_py', 'Y_PY'),
        Variable('Double_t', 'y_pz', 'Y_PZ'),
        Variable('Double_t', 'RandStuff', 'TempStuff'),
    ]
    assert directive['trees']['ATuple']['temp_variables'] == [
        Variable('Double_t', 'TempStuff', 'D0_P+Y_PT'),
    ]


def test_BabyConfigParser_parse_AnotherTuple(realistic_BabyConfigParser):
    directive = realistic_BabyConfigParser.parse()

    assert directive['trees']['AnotherTuple']['input_tree'] == \
        'TupleB0/DecayTree'
    assert directive['trees']['AnotherTuple']['input_branches'] == [
        Variable('Double_t', 'Y_PT'),
        Variable('Double_t', 'Y_PE'),
    ]
    assert directive['trees']['AnotherTuple']['output_branches'] == [
        Variable('Double_t', 'Y_PT', 'Y_PT'),
    ]
    assert directive['system_headers'] == ['cmath', 'iostream']


###################################
# Test individual parse functions #
###################################

@pytest.fixture
def directive():
    return {
        'system_headers': UniqueList(),
        'user_headers': UniqueList(),
        'tree': {},
    }


def test_BabyConfigParser_parse_headers_none(directive,
                                             default_BabyConfigParser):
    default_BabyConfigParser.parse_headers({}, directive)

    assert directive['system_headers'] == []
    assert directive['user_headers'] == []


def test_BabyConfigParser_parse_headers_system_only(directive,
                                                    default_BabyConfigParser):
    default_BabyConfigParser.parse_headers({
        'headers': {
            'system': ['iostream', 'iostream']
        }
    }, directive)

    assert directive['system_headers'] == ['iostream']
    assert directive['user_headers'] == []


def test_BabyConfigParser_parse_headers_user_only(directive,
                                                  default_BabyConfigParser):
    default_BabyConfigParser.parse_headers({
        'headers': {
            'user': ['include/dummy.h']
        }
    }, directive)

    assert directive['system_headers'] == []
    assert directive['user_headers'] == ['include/dummy.h']


def test_BabyConfigParser_parse_drop_keep_rename(default_BabyConfigParser):
    config = {
        'drop': ['Y_P.*'],
        'keep': ['Y_P.*', 'Z_PX', 'X_P.*'],
        'rename': {'Z_PY': 'z_py'}
    }
    dumped_tree = {
        'X_PX': 'float',
        'X_PY': 'float',
        'X_PZ': 'float',
        'Y_PX': 'float',
        'Y_PY': 'float',
        'Y_PZ': 'float',
        'Z_PX': 'float',
        'Z_PY': 'float',
        'Z_PZ': 'float',
    }
    data_store = CppCodeDataStore()

    default_BabyConfigParser.parse_drop_keep_rename(
        config, dumped_tree, data_store)
    assert data_store.input_br == [
        Variable('float', 'X_PX'),
        Variable('float', 'X_PY'),
        Variable('float', 'X_PZ'),
        Variable('float', 'Z_PX'),
        Variable('float', 'Z_PY'),
    ]
    assert data_store.output_br == [
        Variable('float', 'X_PX', 'X_PX'),
        Variable('float', 'X_PY', 'X_PY'),
        Variable('float', 'X_PZ', 'X_PZ'),
        Variable('float', 'Z_PX', 'Z_PX'),
        Variable('float', 'z_py', 'Z_PY'),
    ]


def test_BabyConfigParser_parse_calculation(default_BabyConfigParser):
    config = {
        'calculation': {
            'Y_PX': '^;LOAD',
            'Y_P_TEMP': '^double;Y_PX+1',
            'Y_P_shift': 'double;Y_P_TEMP',
        }
    }
    dumped_tree = {
        'Y_PX': 'float',
        'Y_PY': 'float',
        'Y_PZ': 'float',
    }
    data_store = CppCodeDataStore()

    default_BabyConfigParser.parse_calculation(
        config, dumped_tree, data_store)
    assert data_store.input_br == [Variable('float', 'Y_PX')]
    assert data_store.output_br == [Variable('double', 'Y_P_shift', 'Y_P_TEMP')]
    assert data_store.transient == [Variable('double', 'Y_P_TEMP', 'Y_PX+1')]


def test_BabyConfigParser_parse_load_missing_variables(
        default_BabyConfigParser):
    expr = '!(Y_PX > 10) && FUNCTOR(Y_PY, Y_PZ) != 10'
    dumped_tree = {
        'Y_PX': 'float',
        'Y_PY': 'float',
        'Y_PZ': 'float',
    }
    data_store = CppCodeDataStore()
    default_BabyConfigParser.load_missing_variables(expr, dumped_tree,
                                                    data_store)
    assert data_store.input_br == [
        Variable('float', 'Y_PX'),
        Variable('float', 'Y_PY'),
        Variable('float', 'Y_PZ'),
    ]


def test_BabyConfigParser_parse_selection(default_BabyConfigParser):
    config = {
        'selection': ['Y_PT > 100000', '&&', 'Y_PE > (100 * pow(10, 3))']
    }
    dumped_tree = {
        'Y_PX': 'float',
        'Y_PY': 'float',
        'Y_PZ': 'float',
        'Y_PT': 'float',
        'Y_PE': 'float',
    }
    data_store = CppCodeDataStore()

    default_BabyConfigParser.parse_selection(
        config, dumped_tree, data_store)
    assert data_store.selection == ' '.join(config['selection'])


def test_BabyConfigParser_match_True(default_BabyConfigParser):
    assert default_BabyConfigParser.match(['quick', 'brown', 'fox'], 'fox')


def test_BabyConfigParser_match_False(default_BabyConfigParser):
    assert not default_BabyConfigParser.match(['quick', 'brown', 'fox'], 'Fox')


def test_BabyConfigParser_match_True_inverse(default_BabyConfigParser):
    assert not default_BabyConfigParser.match(['quick', 'brown', 'fox'], 'fox',
                                              False)


def test_BabyConfigParser_match_False_partial_match(default_BabyConfigParser):
    assert not default_BabyConfigParser.match(['quick', 'brown', 'fox2'], 'fox')


def test_BabyConfigParser_match_partial_match(default_BabyConfigParser):
    assert default_BabyConfigParser.match(['quick', 'brown', 'fox'], 'fox2')


def test_BabyConfigParser_LOAD_exist(default_BabyConfigParser):
    dumped_tree = {
        'X_PX': 'float',
        'X_PY': 'float',
        'X_PZ': 'float',
        'Y_PX': 'float',
    }
    data_store = CppCodeDataStore()
    default_BabyConfigParser.LOAD('X_PX', dumped_tree, data_store)
    assert data_store.input_br == [Variable('float', 'X_PX')]


def test_BabyConfigParser_LOAD_not_exist(default_BabyConfigParser):
    dumped_tree = {
        'X_PX': 'float',
        'X_PY': 'float',
        'X_PZ': 'float',
        'Y_PX': 'float',
    }
    data_store = CppCodeDataStore()
    with pytest.raises(KeyError):
        default_BabyConfigParser.LOAD('Z_PX', dumped_tree, data_store)
