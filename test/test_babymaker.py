#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Tue Jan 05, 2021 at 03:08 PM +0100

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


def test_BabyConfigParser_parse_ATuple(realistic_BabyConfigParser):
    directive = realistic_BabyConfigParser.parse()

    assert directive['trees']['ATuple']['input_tree'] == \
        'TupleB0/DecayTree'
    assert directive['trees']['ATuple']['input_branches'] == [
        VariableResolved('Double_t', 'raw_Y_PE', None, 'Y_PE'),
        VariableResolved('Double_t', 'raw_Y_PT', None, 'Y_PT'),
        VariableResolved('Double_t', 'raw_Y_PX', None, 'Y_PX'),
        VariableResolved('Double_t', 'raw_Y_PY', None, 'Y_PY'),
        VariableResolved('Double_t', 'raw_Y_PZ', None, 'Y_PZ'),
        VariableResolved('Double_t', 'raw_D0_P', None, 'D0_P'),
    ]
    assert directive['trees']['ATuple']['output_branches'] == [
        VariableResolved('Double_t', 'keep_Y_PE', 'raw_Y_PE', 'Y_PE'),
        VariableResolved('Double_t', 'rename_y_pt', 'raw_Y_PT', 'y_pt'),
        VariableResolved('Double_t', 'rename_y_px', 'raw_Y_PX', 'y_px'),
        VariableResolved('Double_t', 'rename_y_py', 'raw_Y_PY', 'y_py'),
        VariableResolved('Double_t', 'rename_y_pz', 'raw_Y_PZ', 'y_pz'),
        VariableResolved('Double_t', 'calculation_some_other_var',
                         'calculation_some_var', 'some_other_var'),
        VariableResolved('Double_t', 'calculation_RandStuff',
                         'calculation_TempStuff', 'RandStuff'),
    ]
    assert directive['trees']['ATuple']['transient_vars'] == [
        VariableResolved('Double_t', 'rename_y_pt', 'raw_Y_PT'),
        VariableResolved('Double_t', 'rename_y_px', 'raw_Y_PX'),
        VariableResolved('Double_t', 'rename_y_py', 'raw_Y_PY'),
        VariableResolved('Double_t', 'rename_y_pz', 'raw_Y_PZ'),
        VariableResolved('Double_t', 'calculation_TempStuff',
                         'raw_D0_P+raw_Y_PT'),
        VariableResolved('Double_t', 'calculation_some_var',
                         'rename_y_pt + rename_y_pz',),
        VariableResolved('Double_t', 'calculation_some_other_var',
                         'calculation_some_var'),
        VariableResolved('Double_t', 'calculation_RandStuff',
                         'calculation_TempStuff'),
    ]


def test_BabyConfigParser_parse_AnotherTuple(realistic_BabyConfigParser):
    directive = realistic_BabyConfigParser.parse()

    assert directive['trees']['AnotherTuple']['input_tree'] == \
        'TupleB0/DecayTree'
    assert directive['trees']['AnotherTuple']['input_branches'] == [
        VariableResolved('Double_t', 'raw_Y_PE', None, 'Y_PE'),
        VariableResolved('Double_t', 'raw_Y_PX', None, 'Y_PX'),
        VariableResolved('Double_t', 'raw_Y_PY', None, 'Y_PY'),
        VariableResolved('Double_t', 'raw_Y_PZ', None, 'Y_PZ'),
        VariableResolved('Double_t', 'raw_Y_PT', None, 'Y_PT'),
        VariableResolved('Double_t', 'raw_D0_P', None, 'D0_P'),
    ]
    assert directive['trees']['AnotherTuple']['output_branches'] == [
        VariableResolved('Double_t', 'keep_Y_PE', 'raw_Y_PE', 'Y_PE'),
        VariableResolved('Double_t', 'keep_Y_PX', 'raw_Y_PX', 'Y_PX'),
        VariableResolved('Double_t', 'keep_Y_PY', 'raw_Y_PY', 'Y_PY'),
        VariableResolved('Double_t', 'keep_Y_PZ', 'raw_Y_PZ', 'Y_PZ'),
        VariableResolved('Double_t', 'rename_b0_pt', 'raw_Y_PT', 'b0_pt'),
        VariableResolved('Double_t', 'calculation_RandStuff',
                         'calculation_TempStuff', 'RandStuff'),
        # NOTE: 'some_other_var' is not resolvable for this tree!
        #       Because the change in 'rename' selection, 'y_pt' and 'y_pz' are
        #       not defined!
    ]
    assert directive['system_headers'] == ['cmath', 'iostream']
    assert directive['trees']['AnotherTuple']['selection'] == [
        'true',
        'rename_b0_pt > 10000',
        'raw_Y_PE > (100 * pow(10, 3))'
    ]


def test_BabyConfigParser_parse_YetAnotherTuple(realistic_BabyConfigParser):
    directive = realistic_BabyConfigParser.parse()

    input_branch_names = \
        directive['trees']['YetAnotherTuple']['input_branch_names']
    output_branch_names = \
        directive['trees']['YetAnotherTuple']['output_branch_names']

    assert directive['trees']['YetAnotherTuple']['input_tree'] == \
        'TupleB0WSPi/DecayTree'

    assert 'raw_Y_ISOLATION_CHI22' in input_branch_names
    assert 'raw_Y_ISOLATION_NNp3' in input_branch_names

    assert 'Y_ISOLATION_CHI22' in output_branch_names
    assert 'Y_ISOLATION_NNp3' in output_branch_names

    assert directive['trees']['YetAnotherTuple']['selection'] == [
        'true',
        'raw_piminus_isMuon'
    ]


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
        n: Variable('float', n, n) for n in dumped_tree.keys()
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


def test_BabyConfigParser_resolve_vars_in_scope_keep(
        subdirective, default_BabyConfigParser):
    dumped_tree = {
        'q2': 'float',
        'Y_PX': 'float',
        'Y_PY': 'float',
        'Y_PZ': 'float'
    }
    subdirective['namespace']['raw'] = {v: Variable(t, v)
                                        for v, t in dumped_tree.items()}
    subdirective['namespace']['keep'] = {
        'Y_PX': Variable('float', 'Y_PX', 'Y_PX'),
        'q2': Variable('float', 'q2', 'q2')
    }

    unresolved = default_BabyConfigParser.resolve_vars_in_scope(
        'keep', subdirective['namespace']['keep'], subdirective)

    assert subdirective['transient_vars'] == []
    assert subdirective['output_branches'] == [
        VariableResolved('float', 'keep_Y_PX', 'raw_Y_PX', 'Y_PX'),
        VariableResolved('float', 'keep_q2', 'raw_q2', 'q2'),
    ]
    assert subdirective['loaded_vars'] == [
        'raw_Y_PX',
        'keep_Y_PX',
        'raw_q2',
        'keep_q2',
    ]
    assert unresolved == {}


def test_BabyConfigParser_resolve_vars_in_scope_rename(
        subdirective, default_BabyConfigParser):
    dumped_tree = {
        'q2': 'float',
        'Y_PX': 'float',
        'Y_PY': 'float',
        'Y_PZ': 'float'
    }
    subdirective['namespace']['raw'] = {v: Variable(t, v)
                                        for v, t in dumped_tree.items()}
    subdirective['namespace']['rename'] = {
        'y_px': Variable('float', 'y_px', 'Y_PX'),
        'Q2': Variable('float', 'Q2', 'q2')
    }

    unresolved = default_BabyConfigParser.resolve_vars_in_scope(
        'rename', subdirective['namespace']['rename'], subdirective)

    assert subdirective['transient_vars'] == []
    assert subdirective['output_branches'] == [
        VariableResolved('float', 'rename_y_px', 'raw_Y_PX', 'y_px'),
        VariableResolved('float', 'rename_Q2', 'raw_q2', 'Q2'),
    ]
    assert subdirective['loaded_vars'] == [
        'raw_Y_PX',
        'rename_y_px',
        'raw_q2',
        'rename_Q2',
    ]
    assert unresolved == {}


def test_BabyConfigParser_resolve_vars_in_scope_calculation(
        subdirective, default_BabyConfigParser):
    dumped_tree = {
        'q2': 'float',
        'Y_PX': 'float',
        'Y_PY': 'float',
        'Y_PZ': 'float'
    }
    subdirective['namespace']['raw'] = {v: Variable(t, v)
                                        for v, t in dumped_tree.items()}
    subdirective['namespace']['calculation'] = {
        'y_p_sum': Variable('float', 'y_p_sum', 'Y_PX+Y_PY', transient=True,
                            output=False),
        'q2': Variable('float', 'q2', 'q2 / 1000', transient=True)
    }

    unresolved = default_BabyConfigParser.resolve_vars_in_scope(
        'calculation', subdirective['namespace']['calculation'], subdirective)

    assert subdirective['transient_vars'] == [
        VariableResolved('float', 'calculation_y_p_sum', 'raw_Y_PX+raw_Y_PY'),
        VariableResolved('float', 'calculation_q2', 'raw_q2 / 1000'),
    ]
    assert subdirective['output_branches'] == [
        VariableResolved('float', 'calculation_q2', 'raw_q2 / 1000', 'q2'),
    ]
    assert subdirective['loaded_vars'] == [
        'raw_Y_PX',
        'raw_Y_PY',
        'calculation_y_p_sum',
        'raw_q2',
        'calculation_q2',
    ]
    assert unresolved == {}


def test_BabyConfigParser_resolve_vars_in_scope_calculation_complex(
        subdirective, default_BabyConfigParser):
    dumped_tree = {
        'q2': 'float',
    }
    subdirective['namespace']['raw'] = {v: Variable(t, v)
                                        for v, t in dumped_tree.items()}
    subdirective['namespace']['calculation'] = {
        'q2_diff': Variable('float', 'q2_diff', 'q2_temp', transient=True),
        'q2_temp': Variable('float', 'q2_temp', 'q2 / 1000', transient=True,
                            output=False)
    }

    unresolved = default_BabyConfigParser.resolve_vars_in_scope(
        'calculation', subdirective['namespace']['calculation'], subdirective)

    assert subdirective['transient_vars'] == [
        VariableResolved('float', 'calculation_q2_temp', 'raw_q2 / 1000'),
        VariableResolved('float', 'calculation_q2_diff', 'calculation_q2_temp'),
    ]
    assert subdirective['output_branches'] == [
        VariableResolved('float', 'calculation_q2_diff', 'calculation_q2_temp',
                         'q2_diff'),
    ]
    assert subdirective['loaded_vars'] == [
        'raw_q2',
        'calculation_q2_temp',
        'calculation_q2_diff',
    ]
    assert unresolved == {}
    assert subdirective['namespace']['calculation']['q2_diff'].counter == 2
    assert subdirective['namespace']['calculation']['q2_temp'].counter == 1


def test_BabyConfigParser_resolve_vars_in_scope_calculation_more_complex(
        subdirective, default_BabyConfigParser):
    dumped_tree = {
        'Y_PX': 'float',
        'Y_PY': 'float',
        'Y_PZ': 'float'
    }
    subdirective['namespace']['raw'] = {v: Variable(t, v)
                                        for v, t in dumped_tree.items()}
    subdirective['namespace']['rename'] = {
        'y_px': Variable('float', 'y_px', 'Y_PX', transient=True),
        'y_py': Variable('float', 'y_py', 'Y_PY', transient=True),
    }
    subdirective['namespace']['calculation'] = {
        'y_p_sum': Variable('float', 'y_p_sum', 'y_p_temp', transient=True),
        'y_p_temp': Variable('float', 'y_p_temp', 'y_px + y_py', transient=True,
                             output=False)
    }

    assert default_BabyConfigParser.resolve_vars_in_scope(
        'rename', subdirective['namespace']['rename'], subdirective) == {}

    unresolved = default_BabyConfigParser.resolve_vars_in_scope(
        'calculation', subdirective['namespace']['calculation'], subdirective,
        ['rename']
    )

    assert subdirective['transient_vars'] == [
        VariableResolved('float', 'rename_y_px', 'raw_Y_PX'),
        VariableResolved('float', 'rename_y_py', 'raw_Y_PY'),
        VariableResolved('float', 'calculation_y_p_temp',
                         'rename_y_px + rename_y_py'),
        VariableResolved('float', 'calculation_y_p_sum',
                         'calculation_y_p_temp'),
    ]
    assert subdirective['output_branches'] == [
        VariableResolved('float', 'rename_y_px', 'raw_Y_PX', 'y_px'),
        VariableResolved('float', 'rename_y_py', 'raw_Y_PY', 'y_py'),
        VariableResolved('float', 'calculation_y_p_sum',
                         'calculation_y_p_temp', 'y_p_sum'),
    ]
    assert subdirective['loaded_vars'] == [
        'raw_Y_PX',
        'rename_y_px',
        'raw_Y_PY',
        'rename_y_py',
        'calculation_y_p_temp',
        'calculation_y_p_sum',
    ]
    assert unresolved == {}


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
