#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Wed Sep 01, 2021 at 11:22 PM +0200

import yaml
import pytest

from collections import defaultdict
from os import pardir
from os.path import join as J
from os.path import dirname, realpath

from pyBabyMaker.babymaker import BabyMaker, BabyConfigParser, BabyResolver
from pyBabyMaker.dag_resolver import Node, Variable
from pyBabyMaker.base import UniqueList
from pyBabyMaker.io.NestedYAMLLoader import NestedYAMLLoader
from pyBabyMaker.io.TupleDump import PyTupleDump

PWD = dirname(realpath(__file__))
PARDIR = J(PWD, pardir)
SAMPLE_YAML   = J(PARDIR, 'samples', 'sample-babymaker.yml')
SAMPLE_ROOT   = '../samples/sample.root'
SAMPLE_FRIEND = '../samples/sample_friend.root'
SAMPLE_TMPL   = J(PARDIR, 'pyBabyMaker', 'cpp_templates', 'babymaker.cpp')
SAMPLE_CPP    = J(PARDIR, 'samples', 'sample-babymaker.cpp')


#############################
# Test BabyMaker as a whole #
#############################

def test_BabyMaker_cpp_gen(tmp_path):
    gen_cpp = tmp_path / "gen_cpp.cpp"
    babymaker = BabyMaker(SAMPLE_YAML, SAMPLE_ROOT, [SAMPLE_FRIEND],
                          SAMPLE_TMPL, use_reformatter=False)
    babymaker.gen(gen_cpp, literals={'pi': '3.14'}, debug=True)
    gen_cpp_content = [line.strip()
                       for line in gen_cpp.read_text().split('\n')[1:]]

    with open(SAMPLE_CPP, 'r') as f:
        assert gen_cpp_content == [line.strip() for line in f.readlines()]


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
def realistic_BabyConfigParser(load_files):
    return BabyConfigParser(*load_files, literals={'pi': '3.14'}, debug=True)


def test_BabyConfigParser_parse_ATuple(realistic_BabyConfigParser):
    directive = realistic_BabyConfigParser.parse()

    assert directive['trees']['ATuple']['input_tree'] == 'TupleB0/DecayTree'
    assert directive['trees']['ATuple']['input_br'] == [
        'raw_Y_ISOLATION_BDT',
        'raw_Y_PT',
        'raw_Y_PE',
        'raw_Y_PX',
        'raw_Y_PY',
        'raw_Y_PZ',
        'raw_runNumber',
        'raw_eventNumber',
        'raw_GpsTime',
        'raw_D0_P',
    ]
    assert directive['trees']['ATuple']['input'] == [
        Node('Y_ISOLATION_BDT', 'raw', 'double', input=True, output=False),
        Node('Y_PT', 'raw', 'double', input=True, output=False),
        Node('Y_PE', 'raw', 'double', input=True, output=False),
        Node('Y_PX', 'raw', 'double', input=True, output=False),
        Node('Y_PY', 'raw', 'double', input=True, output=False),
        Node('Y_PZ', 'raw', 'double', input=True, output=False),
        Node('runNumber', 'raw', 'UInt_t', input=True, output=False),
        Node('eventNumber', 'raw', 'ULong64_t', input=True, output=False),
        Node('GpsTime', 'raw', 'ULong64_t', input=True, output=False),
        Node('D0_P', 'raw', 'double', input=True, output=False),
    ]
    assert directive['trees']['ATuple']['output'] == [
        Node('Y_PT', 'keep', 'double', 'Y_PT'),
        Node('Y_PE', 'keep', 'double', 'Y_PE'),
        Node('Y_PX', 'keep', 'double', 'Y_PX'),
        Node('Y_PY', 'keep', 'double', 'Y_PY'),
        Node('Y_PZ', 'keep', 'double', 'Y_PZ'),
        Node('runNumber', 'keep', 'UInt_t', 'runNumber'),
        Node('eventNumber', 'keep', 'ULong64_t', 'eventNumber'),
        Node('GpsTime', 'keep', 'ULong64_t', 'GpsTime'),
        Node('y_pt', 'rename', 'double', 'Y_PT'),
        Node('y_px', 'rename', 'double', 'Y_PX'),
        Node('y_py', 'rename', 'double', 'Y_PY'),
        Node('y_pz', 'rename', 'double', 'Y_PZ'),
        Node('RandStuff', 'calculation', 'double', 'TempStuff*pi'),
        Node('some_other_var', 'calculation', 'double', 'some_var*pi'),
        Node('alt_def', 'calculation', 'double', 'Y_PE'),
    ]
    assert directive['trees']['ATuple']['tmp'] == [
        Node('TempStuff', 'calculation', 'double', 'D0_P+Y_PT', output=False),
        Node('some_var', 'calculation', 'double', 'y_pt + y_pz', output=False),
    ]
    assert directive['trees']['ATuple']['pre_sel_vars'] == []
    assert directive['trees']['ATuple']['post_sel_vars'] == [
        Node('Y_PT', 'keep', 'double', 'Y_PT'),
        Node('Y_PE', 'keep', 'double', 'Y_PE'),
        Node('Y_PX', 'keep', 'double', 'Y_PX'),
        Node('Y_PY', 'keep', 'double', 'Y_PY'),
        Node('Y_PZ', 'keep', 'double', 'Y_PZ'),
        Node('runNumber', 'keep', 'UInt_t', 'runNumber'),
        Node('eventNumber', 'keep', 'ULong64_t', 'eventNumber'),
        Node('GpsTime', 'keep', 'ULong64_t', 'GpsTime'),
        Node('y_pt', 'rename', 'double', 'Y_PT'),
        Node('y_px', 'rename', 'double', 'Y_PX'),
        Node('y_py', 'rename', 'double', 'Y_PY'),
        Node('y_pz', 'rename', 'double', 'Y_PZ'),
        Node('TempStuff', 'calculation', 'double', 'D0_P+Y_PT', output=False),
        Node('RandStuff', 'calculation', 'double', 'TempStuff*pi'),
        Node('some_var', 'calculation', 'double', 'y_pt + y_pz', output=False),
        Node('some_other_var', 'calculation', 'double', 'some_var*pi'),
        Node('alt_def', 'calculation', 'double', 'Y_PE'),
    ]


def test_BabyConfigParser_parse_AnotherTuple(realistic_BabyConfigParser):
    directive = realistic_BabyConfigParser.parse()

    assert directive['trees']['AnotherTuple']['input_tree'] == \
        'TupleB0/DecayTree'
    assert directive['trees']['AnotherTuple']['input'] == [
        Node('Y_ISOLATION_BDT', 'raw', 'double', input=True, output=False),
        Node('Y_PT', 'raw', 'double', input=True, output=False),
        Node('Y_PE', 'raw', 'double', input=True, output=False),
        Node('Y_PX', 'raw', 'double', input=True, output=False),
        Node('Y_PY', 'raw', 'double', input=True, output=False),
        Node('Y_PZ', 'raw', 'double', input=True, output=False),
        Node('runNumber', 'raw', 'UInt_t', input=True, output=False),
        Node('eventNumber', 'raw', 'ULong64_t', input=True, output=False),
        Node('GpsTime', 'raw', 'ULong64_t', input=True, output=False),
        Node('D0_P', 'raw', 'double', input=True, output=False),
    ]
    assert directive['trees']['AnotherTuple']['output'] == [
        # NOTE: 'some_other_var' is not resolvable for this tree!
        #       Because the change in 'rename' selection, 'y_pt' and 'y_pz' are
        #       not defined!
        Node('b0_pt', 'rename', 'double', 'Y_PT'),
        Node('Y_PT', 'keep', 'double', 'Y_PT'),
        Node('Y_PE', 'keep', 'double', 'Y_PE'),
        Node('Y_PX', 'keep', 'double', 'Y_PX'),
        Node('Y_PY', 'keep', 'double', 'Y_PY'),
        Node('Y_PZ', 'keep', 'double', 'Y_PZ'),
        Node('runNumber', 'keep', 'UInt_t', 'runNumber'),
        Node('eventNumber', 'keep', 'ULong64_t', 'eventNumber'),
        Node('GpsTime', 'keep', 'ULong64_t', 'GpsTime'),
        Node('RandStuff', 'calculation', 'double', 'TempStuff*pi'),
    ]
    assert directive['trees']['AnotherTuple']['tmp'] == [
        Node('TempStuff', 'calculation', 'double', 'D0_P+Y_PT', output=False),
    ]
    assert directive['system_headers'] == ['cmath', 'iostream']
    assert directive['trees']['AnotherTuple']['sel'] == [
        'true',
        'raw_Y_ISOLATION_BDT > 0',
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
        'raw_Y_ISOLATION_BDT > 0',
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
        'input_trees': [],
    }


@pytest.fixture
def make_namespace():
    def namespace(dumped_tree):
        ns = defaultdict(dict)
        ns['raw'] = {n: Variable(n, t, input=True)
                     for n, t in dumped_tree.items()}

        return ns
    return namespace


def test_BabyConfigParser_parse_non_existing_tree(directive):
    parsed_yml = {'output': {'nothing': {'input': 'nil'}}}
    dumped_ntuple = {'fake': {'br1': 'double'}}
    parser = BabyConfigParser(parsed_yml, dumped_ntuple)
    directive = parser.parse()

    assert directive['trees'] == {}


def test_BabyConfigParser_parse_headers_none(directive):
    BabyConfigParser.parse_headers({}, directive)

    assert directive['system_headers'] == []
    assert directive['user_headers'] == []


def test_BabyConfigParser_parse_headers_system_only(directive):
    BabyConfigParser.parse_headers({
        'headers': {
            'system': ['iostream', 'iostream']
        }
    }, directive)

    assert directive['system_headers'] == ['iostream']
    assert directive['user_headers'] == []


def test_BabyConfigParser_parse_headers_user_only(directive):
    BabyConfigParser.parse_headers({
        'headers': {
            'user': ['include/dummy.h']
        }
    }, directive)

    assert directive['system_headers'] == []
    assert directive['user_headers'] == ['include/dummy.h']


def test_BabyConfigParser_parse_drop_keep_rename(make_namespace):
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
    BabyConfigParser.parse_drop_keep_rename(config, namespace)

    assert namespace['keep'] == {
        n: Variable(n, 'float', [n]) for n in dumped_tree.keys()
        if not n.startswith('Y') and n != 'Z_PZ' and n != 'Z_PY'}
    assert namespace['rename'] == {
        'z_py': Variable('z_py', 'float', ['Z_PY'])}


def test_BabyConfigParser_parse_calculation(make_namespace):
    config = {'calculation': {
        'Y_P_TEMP': '^double;Y_PX+1',
        'Y_P_shift': 'double;Y_P_TEMP',
    }}
    namespace = make_namespace({})
    BabyConfigParser.parse_calculation(config, namespace)

    assert namespace['calculation'] == {
        'Y_P_TEMP': Variable(
            'Y_P_TEMP', 'double', ['Y_PX+1'], output=False),
        'Y_P_shift': Variable('Y_P_shift', 'double', ['Y_P_TEMP'])
    }


def test_BabyConfigParser_parse_calculation_alt(make_namespace):
    config = {'calculation': {
        'Y_P_TEMP': '^double;Y_PX+1;FUNC(Y_PX, 1)',
    }}
    namespace = make_namespace({})
    BabyConfigParser.parse_calculation(config, namespace)

    assert namespace['calculation'] == {
        'Y_P_TEMP': Variable(
            'Y_P_TEMP', 'double', ['Y_PX+1', 'FUNC(Y_PX, 1)'], output=False)}


def test_BabyConfigParser_parse_calculation_invalid_spec(make_namespace):
    config = {'calculation': {
        'TEMP': '^double Y_PX+1 FUNC(Y_PX, 1)',
    }}
    namespace = make_namespace({})

    with pytest.raises(ValueError) as e:
        BabyConfigParser.parse_calculation(config, namespace)
    assert e.value.args[0] == \
        'Illegal specification for TEMP: ^double Y_PX+1 FUNC(Y_PX, 1).'


############################
# Test variable resolution #
############################

def test_BabyVariableResolver_scope_keep(make_namespace):
    dumped_tree = {
        'q2': 'float',
        'Y_PX': 'float',
        'Y_PY': 'float',
        'Y_PZ': 'float'
    }
    namespace = make_namespace(dumped_tree)
    namespace['keep'] = {
        'Y_PX': Variable('Y_PX', 'float', ['Y_PX']),
        'q2': Variable('q2', 'float', ['q2'])
    }
    resolver = BabyResolver(namespace)
    load_seq, unresolved = resolver.resolve('keep', ordering=['raw'])

    assert load_seq == [
        Node('Y_PX', 'raw', 'float'),
        Node('Y_PX', 'keep', 'float', 'Y_PX'),
        Node('q2', 'raw', 'float'),
        Node('q2', 'keep', 'float', 'q2'),
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
        'y_px': Variable('y_px', 'float', ['Y_PX']),
        'Q2': Variable('Q2', 'float', ['q2'])
    }
    resolver = BabyResolver(namespace)
    load_seq, unresolved = resolver.resolve('rename', ordering=['raw'])

    assert load_seq == [
        Node('Y_PX', 'raw', 'float'),
        Node('y_px', 'rename', 'float', 'Y_PX'),
        Node('q2', 'raw', 'float'),
        Node('Q2', 'rename', 'float', 'q2'),
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
        'y_p_sum': Variable('y_p_sum', 'float', ['Y_PX+Y_PY']),
        'q2': Variable('q2', 'float', ['q2 / 1000'])
    }
    resolver = BabyResolver(namespace)
    load_seq, unresolved = resolver.resolve('calc')

    assert load_seq == [
        Node('Y_PX', 'raw', 'float'),
        Node('Y_PY', 'raw', 'float'),
        Node('y_p_sum', 'calc', 'float', 'Y_PX+Y_PY'),
        Node('q2', 'raw', 'float'),
        Node('q2', 'calc', 'float', 'q2 / 1000'),
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
        'q2_diff': Variable('q2_diff', 'float', ['q2_temp']),
        'q2_temp': Variable('q2_temp', 'float', ['q2 / 1000'], output=False)
    }
    resolver = BabyResolver(namespace)
    load_seq, unresolved = resolver.resolve('calc', ordering=['calc', 'raw'])

    assert load_seq == [
        Node('q2', 'raw', 'float'),
        Node('q2_temp', 'calc', 'float', 'q2 / 1000', output=False),
        Node('q2_diff', 'calc', 'float', 'q2_temp'),
    ]
    assert str(load_seq[2]) == 'float calc_q2_diff = calc_q2_temp'
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
        'y_px': Variable('y_px', 'float', ['Y_PX']),
        'y_py': Variable('y_py', 'float', ['Y_PY']),
    }
    namespace['calc'] = {
        'y_p_sum': Variable('y_p_sum', 'float', ['y_p_temp']),
        'y_p_temp': Variable('y_p_temp', 'float', ['y_px + y_py'])
    }
    resolver = BabyResolver(namespace)
    load_seq, unresolved = resolver.resolve(
        'calc', ordering=['calc', 'rename', 'raw'])

    assert load_seq == [
        Node('Y_PX', 'raw', 'float'),
        Node('y_px', 'rename', 'float', 'Y_PX'),
        Node('Y_PY', 'raw', 'float'),
        Node('y_py', 'rename', 'float', 'Y_PY'),
        Node('y_p_temp', 'calc', 'float', 'y_px + y_py'),
        Node('y_p_sum', 'calc', 'float', 'y_p_temp')
    ]
    assert unresolved == []


##################
# Helper methods #
##################

def test_BabyConfigParser_match_True():
    assert BabyConfigParser.match(['quick', 'brown', 'fox'], 'fox')


def test_BabyConfigParser_match_False():
    assert not BabyConfigParser.match(['quick', 'brown', 'fox'], 'Fox')


def test_BabyConfigParser_match_True_inverse():
    assert not BabyConfigParser.match(['quick', 'brown', 'fox'], 'fox', False)


def test_BabyConfigParser_match_False_partial_match():
    assert not BabyConfigParser.match(['quick', 'brown', 'fox2'], 'fox')


def test_BabyConfigParser_match_partial_match():
    assert BabyConfigParser.match(['quick', 'brown', 'fox'], 'fox2')
