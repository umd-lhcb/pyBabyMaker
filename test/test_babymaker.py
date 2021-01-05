#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Tue Jan 05, 2021 at 01:56 AM +0100

import pytest
import os
import yaml

from collections import defaultdict

from pyBabyMaker.babymaker import Variable, VariableResolved, BabyConfigParser
from pyBabyMaker.base import UniqueList

from pyBabyMaker.io.NestedYAMLLoader import NestedYAMLLoader
from pyBabyMaker.io.TupleDump import PyTupleDump

PWD = os.path.dirname(os.path.realpath(__file__))
PARDIR = os.path.join(PWD, os.pardir)
SAMPLE_YAML = os.path.join(PARDIR, 'samples', 'sample-babymaker.yml')
SAMPLE_ROOT = os.path.join(PARDIR, 'samples', 'sample.root')


######################
# Variable container #
######################

def test_Variable_expr():
    var = Variable('int', 'stuff', 'x+y+(z)*3')
    var.resolved_vars = {'x': 'a_x', 'y': 'b_y', 'z': 'c_z'}
    assert var.expr() == 'a_x+b_y+(c_z)*3'


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


# def test_BabyConfigParser_parse_ATuple(realistic_BabyConfigParser):
    # directive = realistic_BabyConfigParser.parse()

    # assert directive['trees']['ATuple']['input_tree'] == \
        # 'TupleB0/DecayTree'
    # assert directive['trees']['ATuple']['input_branches'] == [
        # Variable('Double_t', 'Y_PT'),
        # Variable('Double_t', 'Y_PE'),
        # Variable('Double_t', 'Y_PX'),
        # Variable('Double_t', 'Y_PY'),
        # Variable('Double_t', 'Y_PZ'),
        # Variable('Double_t', 'D0_P'),
    # ]
    # assert directive['trees']['ATuple']['output_branches'] == [
        # Variable('Double_t', 'y_pt', 'Y_PT'),
        # Variable('Double_t', 'Y_PE', 'Y_PE'),
        # Variable('Double_t', 'y_px', 'Y_PX'),
        # Variable('Double_t', 'y_py', 'Y_PY'),
        # Variable('Double_t', 'y_pz', 'Y_PZ'),
        # Variable('Double_t', 'RandStuff', ' TempStuff', True),
        # Variable('Double_t', 'some_other_var', ' some_var', True),
    # ]
    # assert directive['trees']['ATuple']['transient_vars'] == [
        # Variable('Double_t', 'TempStuff', ' D0_P+Y_PT', True, False),
        # Variable('Double_t', 'RandStuff', ' D0_P+Y_PT', True),
        # Variable('Double_t', 'some_var', ' y_pt + y_pz', True, False),
        # Variable('Double_t', 'some_other_var', ' y_pt + y_pz', True),
    # ]


# def test_BabyConfigParser_parse_AnotherTuple(realistic_BabyConfigParser):
    # directive = realistic_BabyConfigParser.parse()

    # assert directive['trees']['AnotherTuple']['input_tree'] == \
        # 'TupleB0/DecayTree'
    # assert directive['trees']['AnotherTuple']['input_branches'] == [
        # Variable('Double_t', 'Y_PT'),
        # Variable('Double_t', 'Y_PE'),
        # Variable('Double_t', 'Y_PX'),
        # Variable('Double_t', 'Y_PY'),
        # Variable('Double_t', 'Y_PZ'),
        # Variable('Double_t', 'D0_P'),
    # ]
    # assert directive['trees']['AnotherTuple']['output_branches'] == [
        # Variable('Double_t', 'b0_pt', 'Y_PT'),
        # Variable('Double_t', 'Y_PE', 'Y_PE'),
        # Variable('Double_t', 'Y_PX', 'Y_PX'),
        # Variable('Double_t', 'Y_PY', 'Y_PY'),
        # Variable('Double_t', 'Y_PZ', 'Y_PZ'),
        # Variable('Double_t', 'RandStuff', ' TempStuff', True),
        # # NOTE: 'some_other_var' is not resolvable for this tree!
        # #       Because the change in 'rename' selection, 'y_pt' and 'y_pz' are
        # #       not defined!
    # ]
    # assert directive['system_headers'] == ['cmath', 'iostream']


# def test_BabyConfigParser_parse_YetAnotherTuple(realistic_BabyConfigParser):
    # directive = realistic_BabyConfigParser.parse()

    # input_branch_names = \
        # directive['trees']['YetAnotherTuple']['input_branch_names']
    # output_branch_names = [
        # v.name for v in
        # directive['trees']['YetAnotherTuple']['output_branches']]

    # assert directive['trees']['YetAnotherTuple']['input_tree'] == \
        # 'TupleB0WSPi/DecayTree'

    # assert 'Y_ISOLATION_CHI22' in input_branch_names
    # assert 'Y_ISOLATION_NNp3' in input_branch_names

    # assert 'Y_ISOLATION_CHI22' in output_branch_names
    # assert 'Y_ISOLATION_NNp3' in output_branch_names


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
def subdirective():
    return {
        'input_tree': 'sample_tree',
        'namespace': defaultdict(dict),
        'loaded_vars': [],
        'input_branches': [],
        'output_branches': [],
        'transient_vars': [],
        'input_branch_names': [],
        'output_branch_names': []
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
    subdirective['namespace']['raw'] = {n: Variable(t, n)
                                        for n, t in dumped_tree.items()}
    default_BabyConfigParser.parse_drop_keep_rename(config, subdirective)

    assert subdirective['namespace']['keep'] == {
        n: Variable('float', n) for n in dumped_tree.keys()
        if not n.startswith('Y') and n != 'Z_PZ' and n != 'Z_PY'}
    assert subdirective['namespace']['rename'] == {
        'z_py': Variable('float', 'z_py', 'Z_PY', transient=True)
    }


def test_BabyConfigParser_parse_calculation(subdirective,
                                            default_BabyConfigParser):
    config = {'calculation': {
        'Y_P_TEMP': '^double;Y_PX+1',
        'Y_P_shift': 'double;Y_P_TEMP',
    }}
    default_BabyConfigParser.parse_calculation(config, subdirective)

    assert subdirective['namespace']['calculation'] == {
        'Y_P_TEMP': Variable(
            'double', 'Y_P_TEMP', 'Y_PX+1', transient=True, output=False),
        'Y_P_shift': Variable('double', 'Y_P_shift', 'Y_P_TEMP', transient=True)
    }


def test_BabyConfigParser_parse_calculation_alt(subdirective,
                                                default_BabyConfigParser):
    config = {'calculation': {
        'Y_P_TEMP': '^double;Y_PX+1;FUNC(Y_PX, 1)',
    }}
    default_BabyConfigParser.parse_calculation(config, subdirective)

    assert subdirective['namespace']['calculation'] == {
        'Y_P_TEMP': Variable(
            'double', 'Y_P_TEMP', 'Y_PX+1', 'FUNC(Y_PX, 1)',
            transient=True, output=False)
    }


############################
# Test variable resolution #
############################

def test_BabyConfigParser_resolve_var_simple(subdirective,
                                             default_BabyConfigParser):
    dumped_tree = {
        'Y_PX': 'float',
        'Y_PY': 'float',
        'Y_PZ': 'float',
        'Y_PT': 'float',
        'Y_PE': 'float',
    }
    p_sum = Variable('float', 'p_sum', 'Y_PX+Y_PY', transient=True)
    subdirective['namespace']['s'] = {v: Variable(t, v)
                                      for v, t in dumped_tree.items()}
    subdirective['loaded_vars'] = ['s_'+v for v in dumped_tree]

    assert default_BabyConfigParser.resolve_var(
        'test', p_sum, subdirective, ['s'])

    assert subdirective['transient_vars'] == [
        VariableResolved('float', 'test_p_sum', 's_Y_PX+s_Y_PY')]
    assert subdirective['output_branches'] == [
        VariableResolved('float', 'test_p_sum', 's_Y_PX+s_Y_PY', 'p_sum')]
    assert 'p_sum' in subdirective['output_branch_names']


def test_BabyConfigParser_resolve_var_raw(subdirective,
                                          default_BabyConfigParser):
    dumped_tree = {
        'Y_PX': 'float',
        'Y_PY': 'float',
        'Y_PZ': 'float',
        'Y_PT': 'float',
        'Y_PE': 'float',
    }
    p_sum = Variable('float', 'p_sum', 'Y_PX+Y_PY', transient=True)
    subdirective['namespace']['raw'] = {v: Variable(t, v)
                                        for v, t in dumped_tree.items()}
    subdirective['loaded_vars'] = ['raw_'+v for v in dumped_tree]

    assert default_BabyConfigParser.resolve_var(
        'test', p_sum, subdirective, [])

    assert subdirective['transient_vars'] == [
        VariableResolved('float', 'test_p_sum', 'raw_Y_PX+raw_Y_PY')]
    assert subdirective['output_branches'] == [
        VariableResolved('float', 'test_p_sum', 'raw_Y_PX+raw_Y_PY', 'p_sum')]
    assert 'p_sum' in subdirective['output_branch_names']


def test_BabyConfigParser_resolve_var_self(subdirective,
                                           default_BabyConfigParser):
    dumped_tree = {
        'q2': 'float',
    }
    q2 = Variable('float', 'q2', 'GEV2(q2)', transient=True)
    subdirective['namespace']['raw'] = {v: Variable(t, v)
                                        for v, t in dumped_tree.items()}
    subdirective['loaded_vars'] = ['raw_'+v for v in dumped_tree]

    assert default_BabyConfigParser.resolve_var(
        'test', q2, subdirective, [])

    assert subdirective['transient_vars'] == [
        VariableResolved('float', 'test_q2', 'GEV2(raw_q2)')]
    assert subdirective['output_branches'] == [
        VariableResolved('float', 'test_q2', 'GEV2(raw_q2)', 'q2')]
    assert 'q2' in subdirective['output_branch_names']


def test_BabyConfigParser_resolve_var_self_no_resolve(
        subdirective, default_BabyConfigParser):
    q2 = Variable('float', 'q2', 'GEV2(q2)', transient=True)
    subdirective['namespace']['test']['q2'] = q2

    assert not default_BabyConfigParser.resolve_var(
        'test', q2, subdirective, [])


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
