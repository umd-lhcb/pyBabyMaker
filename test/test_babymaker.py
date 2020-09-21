#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Tue Sep 22, 2020 at 02:22 AM +0800

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


##########################
# Parse YAML config file #
##########################

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
        Variable('Double_t', 'RandStuff', ' TempStuff'),
        Variable('Double_t', 'some_other_var', ' some_var'),
    ]
    assert directive['trees']['ATuple']['temp_variables'] == [
        Variable('Double_t', 'TempStuff', ' D0_P+Y_PT'),
        Variable('Double_t', 'some_var', ' y_pt + y_pz'),
    ]


def test_BabyConfigParser_parse_AnotherTuple(realistic_BabyConfigParser):
    directive = realistic_BabyConfigParser.parse()

    assert directive['trees']['AnotherTuple']['input_tree'] == \
        'TupleB0/DecayTree'
    assert directive['trees']['AnotherTuple']['input_branches'] == [
        Variable('Double_t', 'Y_PT'),
        Variable('Double_t', 'Y_PE'),
        Variable('Double_t', 'Y_PX'),
        Variable('Double_t', 'Y_PY'),
        Variable('Double_t', 'Y_PZ'),
        Variable('Double_t', 'D0_P'),
    ]
    assert directive['trees']['AnotherTuple']['output_branches'] == [
        Variable('Double_t', 'b0_pt', 'Y_PT'),
        Variable('Double_t', 'Y_PE', 'Y_PE'),
        Variable('Double_t', 'Y_PX', 'Y_PX'),
        Variable('Double_t', 'Y_PY', 'Y_PY'),
        Variable('Double_t', 'Y_PZ', 'Y_PZ'),
        Variable('Double_t', 'RandStuff', ' TempStuff'),
        # NOTE: 'some_other_var' is not resolvable for this tree!
        #       Because the change in 'rename' selection, 'y_pt' and 'y_pz' are
        #       not defined!
    ]
    assert directive['system_headers'] == ['cmath', 'iostream']


def test_BabyConfigParser_parse_YetAnotherTuple(realistic_BabyConfigParser):
    directive = realistic_BabyConfigParser.parse()

    input_branch_names = \
        directive['trees']['YetAnotherTuple']['input_branch_names']
    output_branch_names = [
        v.name for v in
        directive['trees']['YetAnotherTuple']['output_branches']]

    assert directive['trees']['YetAnotherTuple']['input_tree'] == \
        'TupleB0WSPi/DecayTree'

    assert 'Y_ISOLATION_CHI22' in input_branch_names
    assert 'Y_ISOLATION_NNp3' in input_branch_names

    assert 'Y_ISOLATION_CHI22' in output_branch_names
    assert 'Y_ISOLATION_NNp3' in output_branch_names


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


@pytest.fixture
def subdirective(default_BabyConfigParser):
    return default_BabyConfigParser.gen_subdirective('sample_tree')


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


def test_BabyConfigParser_parse_drop_keep_rename(subdirective,
                                                 default_BabyConfigParser):
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
    default_BabyConfigParser.parse_drop_keep_rename(
        config, dumped_tree, subdirective)

    assert subdirective['input_branches'] == [
        Variable('float', 'X_PX'),
        Variable('float', 'X_PY'),
        Variable('float', 'X_PZ'),
        Variable('float', 'Z_PX'),
        Variable('float', 'Z_PY'),
    ]
    assert subdirective['output_branches'] == [
        Variable('float', 'X_PX', 'X_PX'),
        Variable('float', 'X_PY', 'X_PY'),
        Variable('float', 'X_PZ', 'X_PZ'),
        Variable('float', 'Z_PX', 'Z_PX'),
        Variable('float', 'z_py', 'Z_PY'),
    ]


def test_BabyConfigParser_parse_calculation(subdirective,
                                            default_BabyConfigParser):
    config = {
        'calculation': {
            'Y_P_TEMP': '^double;Y_PX+1',
            'Y_P_shift': 'double;Y_P_TEMP',
        }
    }
    default_BabyConfigParser.parse_calculation(
        config, subdirective)

    assert subdirective['input_branches'] == []  # Dependency is resolved later
    assert subdirective['output_branches'] == [
        Variable('double', 'Y_P_shift', 'Y_P_TEMP')]
    assert subdirective['temp_variables'] == [
        Variable('double', 'Y_P_TEMP', 'Y_PX+1')]


def test_BabyConfigParser_parse_load_missing_vars(
        subdirective, default_BabyConfigParser):
    expr = '!(Y_PX > 10) && FUNCTOR(Y_PY, Y_PZ) != 10'
    dumped_tree = {
        'Y_PX': 'float',
        'Y_PY': 'float',
        'Y_PZ': 'float',
    }
    default_BabyConfigParser.load_missing_vars(
        expr, dumped_tree, subdirective)
    assert subdirective['input_branches'] == [
        Variable('float', 'Y_PY'),
        Variable('float', 'Y_PZ'),
        Variable('float', 'Y_PX'),
    ]


def test_BabyConfigParser_parse_selection(subdirective,
                                          default_BabyConfigParser):
    config = {
        'selection': ['Y_PT > 100000', 'Y_PE > (100 * pow(10, 3))']
    }
    dumped_tree = {
        'Y_PX': 'float',
        'Y_PY': 'float',
        'Y_PZ': 'float',
        'Y_PT': 'float',
        'Y_PE': 'float',
    }
    default_BabyConfigParser.parse_selection(
        config, dumped_tree, subdirective)

    assert subdirective['selection'] == config['selection']


##################
# Helper methods #
##################

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


def test_BabyConfigParser_load_missing_vars(subdirective,
                                            default_BabyConfigParser):
    subdirective['known_names'] = ['TempStuff']
    dumped_tree = {
        'X_PX': 'float',
        'X_PY': 'float',
        'X_PZ': 'float',
        'Y_PX': 'float',
    }
    default_BabyConfigParser.load_missing_vars('X_PX+TempStuff', dumped_tree,
                                               subdirective)

    assert subdirective['known_names'] == ['TempStuff', 'X_PX']


def test_BabyConfigParser_load_var_exist(default_BabyConfigParser):
    dumped_tree = {
        'X_PX': 'float',
        'X_PY': 'float',
        'X_PZ': 'float',
        'Y_PX': 'float',
    }
    result = default_BabyConfigParser.load_var('X_PX', dumped_tree)

    assert result == 'float'


def test_BabyConfigParser_load_var_not_exist(default_BabyConfigParser):
    dumped_tree = {
        'X_PX': 'float',
        'X_PY': 'float',
        'X_PZ': 'float',
        'Y_PX': 'float',
    }
    with pytest.raises(KeyError):
        default_BabyConfigParser.load_var('Z_PX', dumped_tree)


def test_BabyConfigParser_var_load_seq_normal(default_BabyConfigParser):
    known_names = ['a', 'b']
    vars_to_load = [
        Variable('int', 'temp3', 'temp1+temp2'),
        Variable('int', 'temp1', 'a+c'),
        Variable('int', 'temp2', 'temp1+d'),
    ]
    dumped_tree = {'c': 'int', 'd': int}
    directive = {'input_branches': [], 'known_names': known_names}
    transient_vars, vars_to_load = default_BabyConfigParser.var_load_seq(
        vars_to_load, dumped_tree, directive)

    assert vars_to_load == []
    assert transient_vars == [
        Variable('int', 'temp1', 'a+c'),
        Variable('int', 'temp2', 'temp1+d'),
        Variable('int', 'temp3', 'temp1+temp2'),
    ]
    assert known_names == ['a', 'b', 'c', 'temp1', 'd', 'temp2', 'temp3']


def test_BabyConfigParser_var_load_seq_circular(default_BabyConfigParser):
    known_names = ['a', 'b']
    vars_to_load = [
        Variable('int', 'temp1', 'temp2'),
        Variable('int', 'temp2', 'temp1+d'),
    ]
    dumped_tree = {'c': 'int', 'd': int}
    directive = {'input_branches': [], 'known_names': known_names}
    transient_vars, vars_to_load = default_BabyConfigParser.var_load_seq(
        vars_to_load, dumped_tree, directive)

    assert vars_to_load == [
        Variable('int', 'temp1', 'temp2'),
        Variable('int', 'temp2', 'temp1+d'),
    ]
    assert transient_vars == []
    # NOTE: Due to my desire to do fewer number of recursions when resolving
    #       dependency, I pay the price of loading not really needed branches.
    assert known_names == ['a', 'b', 'd']
