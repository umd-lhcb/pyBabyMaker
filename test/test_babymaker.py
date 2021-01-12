#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Wed Jan 13, 2021 at 12:33 AM +0100

import pytest
import os
import yaml

from collections import defaultdict

from pyBabyMaker.babymaker import BabyVariable, BabyConfigParser, \
    BabyVariableResolver
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

def test_BabyVariable_default():
    var = BabyVariable('stuff')

    assert var.input is False
    assert var.output is True
    assert var.rval == ''


def test_BabyVariable_set_fname():
    var = BabyVariable('stuff')
    assert var.fname == 'stuff'

    var.fname = 'test_stuff'
    assert var.fname == 'test_stuff'

    var.fname = 'fake_stuff'
    assert var.fname == 'test_stuff'


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

    assert directive['trees']['ATuple']['input_tree'] == 'TupleB0/DecayTree'
    assert directive['trees']['ATuple']['input_br'] == [
        'raw_Y_PT',
        'raw_Y_PE',
        'raw_Y_PX',
        'raw_Y_PY',
        'raw_Y_PZ',
        'raw_D0_P',
    ]
    assert directive['trees']['ATuple']['input'] == [
        BabyVariable('Y_PT', 'Double_t', input=True, output=False),
        BabyVariable('Y_PE', 'Double_t', input=True, output=False),
        BabyVariable('Y_PX', 'Double_t', input=True, output=False),
        BabyVariable('Y_PY', 'Double_t', input=True, output=False),
        BabyVariable('Y_PZ', 'Double_t', input=True, output=False),
        BabyVariable('D0_P', 'Double_t', input=True, output=False),
    ]
    assert directive['trees']['ATuple']['output'] == [
        BabyVariable('Y_PE', 'Double_t', ['Y_PE']),
        BabyVariable('y_pt', 'Double_t', ['Y_PT']),
        BabyVariable('y_px', 'Double_t', ['Y_PX']),
        BabyVariable('y_py', 'Double_t', ['Y_PY']),
        BabyVariable('y_pz', 'Double_t', ['Y_PZ']),
        BabyVariable('RandStuff', 'Double_t', ['TempStuff']),
        BabyVariable('some_other_var', 'Double_t', ['some_var']),
        BabyVariable('alt_def', 'Double_t', ['b0_pe', 'Y_PE']),
    ]
    assert directive['trees']['ATuple']['tmp'] == [
        BabyVariable('TempStuff', 'Double_t', ['D0_P+Y_PT'], output=False),
        BabyVariable('some_var', 'Double_t', ['y_pt + y_pz'], output=False),
    ]
    assert directive['trees']['ATuple']['pre_sel_vars'] == []
    assert directive['trees']['ATuple']['post_sel_vars'] == [
        BabyVariable('Y_PE', 'Double_t', ['Y_PE']),
        BabyVariable('y_pt', 'Double_t', ['Y_PT']),
        BabyVariable('y_px', 'Double_t', ['Y_PX']),
        BabyVariable('y_py', 'Double_t', ['Y_PY']),
        BabyVariable('y_pz', 'Double_t', ['Y_PZ']),
        BabyVariable('TempStuff', 'Double_t', ['D0_P+Y_PT'], output=False),
        BabyVariable('RandStuff', 'Double_t', ['TempStuff']),
        BabyVariable('some_var', 'Double_t', ['y_pt + y_pz'], output=False),
        BabyVariable('some_other_var', 'Double_t', ['some_var']),
        BabyVariable('alt_def', 'Double_t', ['b0_pe', 'Y_PE']),
    ]


def test_BabyConfigParser_parse_AnotherTuple(realistic_BabyConfigParser):
    directive = realistic_BabyConfigParser.parse()

    assert directive['trees']['AnotherTuple']['input_tree'] == \
        'TupleB0/DecayTree'
    assert directive['trees']['AnotherTuple']['input'] == [
        BabyVariable('Y_PT', 'Double_t', input=True, output=False),
        BabyVariable('Y_PE', 'Double_t', input=True, output=False),
        BabyVariable('Y_PX', 'Double_t', input=True, output=False),
        BabyVariable('Y_PY', 'Double_t', input=True, output=False),
        BabyVariable('Y_PZ', 'Double_t', input=True, output=False),
        BabyVariable('D0_P', 'Double_t', input=True, output=False),
    ]
    assert directive['trees']['AnotherTuple']['output'] == [
        # NOTE: 'some_other_var' is not resolvable for this tree!
        #       Because the change in 'rename' selection, 'y_pt' and 'y_pz' are
        #       not defined!
        BabyVariable('b0_pt', 'Double_t', ['Y_PT']),
        BabyVariable('Y_PE', 'Double_t', ['Y_PE']),
        BabyVariable('Y_PX', 'Double_t', ['Y_PX']),
        BabyVariable('Y_PY', 'Double_t', ['Y_PY']),
        BabyVariable('Y_PZ', 'Double_t', ['Y_PZ']),
        BabyVariable('RandStuff', 'Double_t', ['TempStuff']),
    ]
    assert directive['trees']['AnotherTuple']['tmp'] == [
        BabyVariable('TempStuff', 'Double_t', ['D0_P+Y_PT'], output=False),
    ]
    assert directive['system_headers'] == ['cmath', 'iostream']
    assert directive['trees']['AnotherTuple']['sel'] == [
        'true',
        'rename_b0_pt > 10000',
        'raw_Y_PE > (100 * pow(10, 3))'
    ]


def test_BabyConfigParser_parse_YetAnotherTuple(realistic_BabyConfigParser):
    directive = realistic_BabyConfigParser.parse()
    input_br = directive['trees']['YetAnotherTuple']['input_br']

    assert directive['trees']['YetAnotherTuple']['input_tree'] == \
        'TupleB0WSPi/DecayTree'
    assert 'raw_Y_ISOLATION_CHI22' in input_br
    assert 'raw_Y_ISOLATION_NNp3' in input_br
    assert directive['trees']['YetAnotherTuple']['sel'] == [
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
def make_namespace():
    def namespace(dumped_tree):
        ns = defaultdict(dict)
        ns['raw'] = {n: BabyVariable(n, t, input=True)
                     for n, t in dumped_tree.items()}

        return ns
    return namespace


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


def test_BabyConfigParser_parse_drop_keep_rename(make_namespace,
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
    namespace = make_namespace(dumped_tree)
    default_BabyConfigParser.parse_drop_keep_rename(config, namespace)

    assert namespace['keep'] == {
        n: BabyVariable(n, 'float', [n]) for n in dumped_tree.keys()
        if not n.startswith('Y') and n != 'Z_PZ' and n != 'Z_PY'}
    assert namespace['rename'] == {
        'z_py': BabyVariable('z_py', 'float', ['Z_PY'])}


def test_BabyConfigParser_parse_calculation(make_namespace,
                                            default_BabyConfigParser):
    config = {'calculation': {
        'Y_P_TEMP': '^double;Y_PX+1',
        'Y_P_shift': 'double;Y_P_TEMP',
    }}
    namespace = make_namespace({})
    default_BabyConfigParser.parse_calculation(config, namespace)

    assert namespace['calculation'] == {
        'Y_P_TEMP': BabyVariable(
            'Y_P_TEMP', 'double', ['Y_PX+1'], output=False),
        'Y_P_shift': BabyVariable('Y_P_shift', 'double', ['Y_P_TEMP'])
    }


def test_BabyConfigParser_parse_calculation_alt(make_namespace,
                                                default_BabyConfigParser):
    config = {'calculation': {
        'Y_P_TEMP': '^double;Y_PX+1;FUNC(Y_PX, 1)',
    }}
    namespace = make_namespace({})
    default_BabyConfigParser.parse_calculation(config, namespace)

    assert namespace['calculation'] == {
        'Y_P_TEMP': BabyVariable(
            'Y_P_TEMP', 'double', ['Y_PX+1', 'FUNC(Y_PX, 1)'], output=False)}


############################
# Test variable resolution #
############################

def test_BabyVariableResolver_simple(make_namespace):
    dumped_tree = {
        'Y_PX': 'float',
        'Y_PY': 'float',
        'Y_PZ': 'float',
        'Y_PT': 'float',
        'Y_PE': 'float',
    }
    namespace = make_namespace(dumped_tree)
    var = BabyVariable('p_sum', 'float', ['Y_PX+Y_PY'])
    resolver = BabyVariableResolver(namespace)
    status, load_seq, known_names = resolver.resolve_var('test', var)

    assert status is True
    assert load_seq == [
        namespace['raw']['Y_PX'],
        namespace['raw']['Y_PY'],
        var
    ]
    assert load_seq[2].rval == 'raw_Y_PX+raw_Y_PY'
    assert load_seq[2].name == 'p_sum'
    assert load_seq[2].fname == 'test_p_sum'


def test_BabyVariableResolver_self(make_namespace):
    dumped_tree = {
        'q2': 'float',
    }
    namespace = make_namespace(dumped_tree)
    var = BabyVariable('q2', 'float', ['GEV2(q2)'])
    namespace['test']['q2'] = var
    resolver = BabyVariableResolver(namespace)
    status, load_seq, known_names = resolver.resolve_var(
        'test', var, ['test', 'raw'])

    assert status is True
    assert load_seq == [
        namespace['raw']['q2'],
        var
    ]


def test_BabyVariableResolver_self_no_resolve(make_namespace):
    namespace = make_namespace({})
    var = BabyVariable('q2', 'float', ['GEV2(q2)'])
    namespace['test']['q2'] = var
    resolver = BabyVariableResolver(namespace)
    status, load_seq, known_names = resolver.resolve_var(
        'test', var, ['test', 'raw'])

    assert status is False


def test_BabyVariableResolver_scope_keep(make_namespace):
    dumped_tree = {
        'q2': 'float',
        'Y_PX': 'float',
        'Y_PY': 'float',
        'Y_PZ': 'float'
    }
    namespace = make_namespace(dumped_tree)
    namespace['keep'] = {
        'Y_PX': BabyVariable('Y_PX', 'float', ['Y_PX']),
        'q2': BabyVariable('q2', 'float', ['q2'])
    }
    resolver = BabyVariableResolver(namespace)
    load_seq, unresolved = resolver.resolve_scope('keep', ordering=['raw'])

    assert load_seq == [
        namespace['raw']['Y_PX'],
        namespace['keep']['Y_PX'],
        namespace['raw']['q2'],
        namespace['keep']['q2'],
    ]
    assert unresolved == []


def test_BabyVariableResolver_scope_rename(make_namespace):
    dumped_tree = {
        'q2': 'float',
        'Y_PX': 'float',
        'Y_PY': 'float',
        'Y_PZ': 'float'
    }
    namespace = make_namespace(dumped_tree)
    namespace['rename'] = {
        'y_px': BabyVariable('y_px', 'float', ['Y_PX']),
        'Q2': BabyVariable('Q2', 'float', ['q2'])
    }
    resolver = BabyVariableResolver(namespace)
    load_seq, unresolved = resolver.resolve_scope('rename', ordering=['raw'])

    assert load_seq == [
        namespace['raw']['Y_PX'],
        namespace['rename']['y_px'],
        namespace['raw']['q2'],
        namespace['rename']['Q2'],
    ]
    assert load_seq[3].rval == 'raw_q2'
    assert load_seq[3].name == 'Q2'
    assert load_seq[3].fname == 'rename_Q2'
    assert unresolved == []


def test_BabyVariableResolver_scope_calculation(make_namespace):
    dumped_tree = {
        'q2': 'float',
        'Y_PX': 'float',
        'Y_PY': 'float',
        'Y_PZ': 'float'
    }
    namespace = make_namespace(dumped_tree)
    namespace['calc'] = {
        'y_p_sum': BabyVariable('y_p_sum', 'float', ['Y_PX+Y_PY']),
        'q2': BabyVariable('q2', 'float', ['q2 / 1000'])
    }
    resolver = BabyVariableResolver(namespace)
    load_seq, unresolved = resolver.resolve_scope('calc')

    assert load_seq == [
        namespace['raw']['Y_PX'],
        namespace['raw']['Y_PY'],
        namespace['calc']['y_p_sum'],
        namespace['raw']['q2'],
        namespace['calc']['q2'],
    ]
    assert load_seq[2].rval == 'raw_Y_PX+raw_Y_PY'
    assert load_seq[4].rval == 'raw_q2 / 1000'
    assert load_seq[4].fname == 'calc_q2'
    assert load_seq[4].name == 'q2'
    assert unresolved == []


def test_BabyVariableResolver_scope_calculation_complex(make_namespace):
    dumped_tree = {
        'q2': 'float',
    }
    namespace = make_namespace(dumped_tree)
    namespace['calc'] = {
        'q2_diff': BabyVariable('q2_diff', 'float', ['q2_temp']),
        'q2_temp': BabyVariable('q2_temp', 'float', ['q2 / 1000'], output=False)
    }
    resolver = BabyVariableResolver(namespace)
    load_seq, unresolved = resolver.resolve_scope('calc')

    assert load_seq == [
        namespace['raw']['q2'],
        namespace['calc']['q2_temp'],
        namespace['calc']['q2_diff'],
    ]
    assert str(load_seq[2]) == 'float q2_diff = q2_temp'
    assert load_seq[2].fname == 'calc_q2_diff'
    assert load_seq[2].rval == 'calc_q2_temp'
    assert unresolved == []


def test_BabyVariableResolver_scope_calculation_more_complex(make_namespace):
    dumped_tree = {
        'Y_PX': 'float',
        'Y_PY': 'float',
        'Y_PZ': 'float'
    }
    namespace = make_namespace(dumped_tree)
    namespace['rename'] = {
        'y_px': BabyVariable('y_px', 'float', ['Y_PX']),
        'y_py': BabyVariable('y_py', 'float', ['Y_PY']),
    }
    namespace['calc'] = {
        'y_p_sum': BabyVariable('y_p_sum', 'float', ['y_p_temp']),
        'y_p_temp': BabyVariable('y_p_temp', 'float', ['y_px + y_py'])
    }
    resolver = BabyVariableResolver(namespace)
    load_seq, unresolved = resolver.resolve_scope('calc')

    assert load_seq == [
        namespace['raw']['Y_PX'],
        namespace['rename']['y_px'],
        namespace['raw']['Y_PY'],
        namespace['rename']['y_py'],
        namespace['calc']['y_p_temp'],
        namespace['calc']['y_p_sum'],
    ]
    assert unresolved == []


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
