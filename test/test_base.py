#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Mon Sep 09, 2019 at 12:09 AM -0400

import pytest
import os
import yaml

from unittest.mock import patch
from datetime import datetime

from pyBabyMaker.base import UniqueList
from pyBabyMaker.base import Variable, CppCodeDataStore
from pyBabyMaker.base import BaseConfigParser
from pyBabyMaker.base import BaseCppGenerator
from pyBabyMaker.base import BaseMaker

from pyBabyMaker.io.NestedYAMLLoader import NestedYAMLLoader
from pyBabyMaker.io.TupleDump import PyTupleDump

PWD = os.path.dirname(os.path.realpath(__file__))
PARDIR = os.path.join(PWD, os.pardir)
SAMPLE_YAML = os.path.join(PARDIR, 'samples', 'sample-babymaker.yml')
SAMPLE_ROOT = os.path.join(PARDIR, 'samples', 'sample.root')


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


# CppCodeDataStore #############################################################

@pytest.fixture
def default_CppCodeDataStore():
    return CppCodeDataStore()


def test_CppCodeDataStore_append_correct(default_CppCodeDataStore):
    variable = Variable('float', 'a', '1')
    default_CppCodeDataStore.append(variable, 'input_br')
    assert default_CppCodeDataStore.input_br == [variable]


def test_CppCodeDataStore_append_wrong_type(default_CppCodeDataStore):
    variable = 'variable'
    with pytest.raises(TypeError):
        default_CppCodeDataStore.append(variable, 'input_br')


def test_CppCodeDataStore_append_wrong_list(default_CppCodeDataStore):
    variable = Variable('float', 'a', '1')
    with pytest.raises(AttributeError):
        default_CppCodeDataStore.append(variable, 'test')


def test_CppCodeDataStore_append_input(default_CppCodeDataStore):
    variable = Variable('float', 'a', '1')
    default_CppCodeDataStore.append_input_br(variable)
    assert default_CppCodeDataStore.input_br == [variable]


def test_CppCodeDataStore_append_output(default_CppCodeDataStore):
    variable = Variable('float', 'a', '1')
    default_CppCodeDataStore.append_output_br(variable)
    assert default_CppCodeDataStore.output_br == [variable]


def test_CppCodeDataStore_append_transient(default_CppCodeDataStore):
    variable = Variable('float', 'a', '1')
    default_CppCodeDataStore.append_transient(variable)
    assert default_CppCodeDataStore.transient == [variable]


###########
# Parsers #
###########

@pytest.fixture
def load_files():
    with open(SAMPLE_YAML) as f:
        parsed_config = yaml.load(f, NestedYAMLLoader)
    dumped_ntuple = PyTupleDump(SAMPLE_ROOT).dump()
    return (parsed_config, dumped_ntuple)


@pytest.fixture
def default_BaseConfigParser():
    return BaseConfigParser(None, None)


@pytest.fixture
def realistic_BaseConfigParser(load_files):
    return BaseConfigParser(*load_files)


def test_BaseConfigParser_parse_ATuple(realistic_BaseConfigParser):
    realistic_BaseConfigParser.parse()
    assert realistic_BaseConfigParser.instructions[0].input_tree == \
        'TupleB0/DecayTree'
    assert realistic_BaseConfigParser.instructions[0].output_tree == \
        'ATuple'
    assert realistic_BaseConfigParser.instructions[0].input_br == [
        Variable('Double_t', 'Y_PT'),
        Variable('Double_t', 'Y_PE'),
        Variable('Double_t', 'Y_PX'),
        Variable('Double_t', 'Y_PY'),
        Variable('Double_t', 'Y_PZ'),
        Variable('Double_t', 'D0_P'),
    ]
    assert realistic_BaseConfigParser.instructions[0].output_br == [
        Variable('Double_t', 'y_pt', 'Y_PT'),
        Variable('Double_t', 'Y_PE', 'Y_PE'),
        Variable('Double_t', 'y_px', 'Y_PX'),
        Variable('Double_t', 'y_py', 'Y_PY'),
        Variable('Double_t', 'y_pz', 'Y_PZ'),
        Variable('Double_t', 'RandStuff', 'TempStuff'),
    ]
    assert realistic_BaseConfigParser.instructions[0].transient == [
        Variable('Double_t', 'TempStuff', 'D0_P+Y_PT'),
    ]


def test_BaseConfigParser_parse_AnotherTuple(realistic_BaseConfigParser):
    realistic_BaseConfigParser.parse()
    assert realistic_BaseConfigParser.instructions[1].input_tree == \
        'TupleB0/DecayTree'
    assert realistic_BaseConfigParser.instructions[1].output_tree == \
        'AnotherTuple'
    assert realistic_BaseConfigParser.instructions[1].input_br == [
        Variable('Double_t', 'Y_PT'),
        Variable('Double_t', 'Y_PE'),
    ]
    assert realistic_BaseConfigParser.instructions[1].output_br == [
        Variable('Double_t', 'Y_PT', 'Y_PT'),
    ]
    assert realistic_BaseConfigParser.system_headers == ['cmath', 'iostream']


def test_BaseConfigParser_parse_headers_none(default_BaseConfigParser):
    default_BaseConfigParser.parse_headers({})
    assert default_BaseConfigParser.system_headers == []
    assert default_BaseConfigParser.user_headers == []


def test_BaseConfigParser_parse_headers_system_only(default_BaseConfigParser):
    default_BaseConfigParser.parse_headers({
        'headers': {
            'system': ['iostream', 'iostream']
        }
    })
    assert default_BaseConfigParser.system_headers == ['iostream']
    assert default_BaseConfigParser.user_headers == []


def test_BaseConfigParser_parse_headers_user_only(default_BaseConfigParser):
    default_BaseConfigParser.parse_headers({
        'headers': {
            'user': ['include/dummy.h']
        }
    })
    assert default_BaseConfigParser.system_headers == []
    assert default_BaseConfigParser.user_headers == ['include/dummy.h']


def test_BaseConfigParser_parse_drop_keep_rename(default_BaseConfigParser):
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

    default_BaseConfigParser.parse_drop_keep_rename(
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


def test_BaseConfigParser_parse_calculation(default_BaseConfigParser):
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

    default_BaseConfigParser.parse_calculation(
        config, dumped_tree, data_store)
    assert data_store.input_br == [Variable('float', 'Y_PX')]
    assert data_store.output_br == [Variable('double', 'Y_P_shift', 'Y_P_TEMP')]
    assert data_store.transient == [Variable('double', 'Y_P_TEMP', 'Y_PX+1')]


def test_BaseConfigParser_parse_load_missing_variables(
        default_BaseConfigParser):
    expr = '!(Y_PX > 10) && FUNCTOR(Y_PY, Y_PZ) != 10'
    dumped_tree = {
        'Y_PX': 'float',
        'Y_PY': 'float',
        'Y_PZ': 'float',
    }
    data_store = CppCodeDataStore()
    default_BaseConfigParser.load_missing_variables(expr, dumped_tree,
                                                    data_store)
    assert data_store.input_br == [
        Variable('float', 'Y_PX'),
        Variable('float', 'Y_PY'),
        Variable('float', 'Y_PZ'),
    ]


def test_BaseConfigParser_parse_selection(default_BaseConfigParser):
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

    default_BaseConfigParser.parse_selection(
        config, dumped_tree, data_store)
    assert data_store.selection == ' '.join(config['selection'])


def test_BaseConfigParser_match_True(default_BaseConfigParser):
    assert default_BaseConfigParser.match(['quick', 'brown', 'fox'], 'fox')


def test_BaseConfigParser_match_False(default_BaseConfigParser):
    assert not default_BaseConfigParser.match(['quick', 'brown', 'fox'], 'Fox')


def test_BaseConfigParser_match_True_inverse(default_BaseConfigParser):
    assert not default_BaseConfigParser.match(['quick', 'brown', 'fox'], 'fox',
                                              False)


def test_BaseConfigParser_match_False_partial_match(default_BaseConfigParser):
    assert not default_BaseConfigParser.match(['quick', 'brown', 'fox2'], 'fox')


def test_BaseConfigParser_match_partial_match(default_BaseConfigParser):
    assert default_BaseConfigParser.match(['quick', 'brown', 'fox'], 'fox2')


def test_BaseConfigParser_LOAD_exist(default_BaseConfigParser):
    dumped_tree = {
        'X_PX': 'float',
        'X_PY': 'float',
        'X_PZ': 'float',
        'Y_PX': 'float',
    }
    data_store = CppCodeDataStore()
    default_BaseConfigParser.LOAD('X_PX', dumped_tree, data_store)
    assert data_store.input_br == [Variable('float', 'X_PX')]


def test_BaseConfigParser_LOAD_not_exist(default_BaseConfigParser):
    dumped_tree = {
        'X_PX': 'float',
        'X_PY': 'float',
        'X_PZ': 'float',
        'Y_PX': 'float',
    }
    data_store = CppCodeDataStore()
    with pytest.raises(KeyError):
        default_BaseConfigParser.LOAD('Z_PX', dumped_tree, data_store)


#######################
# C++ code generators #
#######################

class SimpleCppGenerator(BaseCppGenerator):
    def gen(self):
        pass

    def gen_preamble(self):
        pass

    def gen_body(self):
        pass


@pytest.fixture
def default_SimpleCppGenerator():
    return SimpleCppGenerator(
        list(),
        additional_system_headers=['iostream'],
        additional_user_headers=['include/dummy.h']
    )


# Headers ######################################################################

def test_SimpleCppGenerator_custom_system_headers(default_SimpleCppGenerator):
    assert default_SimpleCppGenerator.system_headers == \
        ['TFile.h', 'TTree.h', 'TTreeReader.h', 'TBranch.h', 'iostream']


def test_SimpleCppGenerator_custom_user_headers(default_SimpleCppGenerator):
    assert default_SimpleCppGenerator.user_headers == ['include/dummy.h']


def test_SimpleCppGenerator_gen_headers(default_SimpleCppGenerator):
    assert default_SimpleCppGenerator.gen_headers() == \
        '''#include <TFile.h>
#include <TTree.h>
#include <TTreeReader.h>
#include <TBranch.h>
#include <iostream>

#include "include/dummy.h"
'''


def test_SimpleCppGenerator_gen_headers_no_user():
    cpp_generator = SimpleCppGenerator(None)
    assert cpp_generator.gen_headers() == \
        '''#include <TFile.h>
#include <TTree.h>
#include <TTreeReader.h>
#include <TBranch.h>

'''


# Helpers ######################################################################

def test_SimpleCppGenerator_dereference_variables_simple(
        default_SimpleCppGenerator):
    assert default_SimpleCppGenerator.dereference_variables(
        'a > b_1 && b_1 < c', [Variable('int', 'a'), Variable('int', 'b_1'),
                               Variable('int', 'c')]
    ) == '(*a) > (*b_1) && (*b_1) < (*c)'


def test_SimpleCppGenerator_dereference_variables_duplicate(
        default_SimpleCppGenerator):
    assert default_SimpleCppGenerator.dereference_variables(
        'a > b_1 && b_1 < c', [Variable('int', 'a'), Variable('int', 'b_1'),
                               Variable('int', 'c'), Variable('int', 'b_1')]
    ) == '(*a) > (*b_1) && (*b_1) < (*c)'


# C++ snippets #################################################################

def test_SimpleCppGenerator_cpp_gen_date(default_SimpleCppGenerator):
    with patch('pyBabyMaker.base.datetime') as m:
        m.now.return_value = datetime(2019, 8, 31, 3, 46, 15, 98809)
        assert default_SimpleCppGenerator.cpp_gen_date() == \
            '// Generated on: 2019-08-31 03:46:15.098809\n'


def test_SimpleCppGenerator_cpp_header_system(default_SimpleCppGenerator):
    assert default_SimpleCppGenerator.cpp_header('iostream') == \
        '#include <iostream>\n'


def test_SimpleCppGenerator_cpp_header_user(default_SimpleCppGenerator):
    assert default_SimpleCppGenerator.cpp_header('include/dummy.h', False) == \
        '#include "include/dummy.h"\n'


def test_SimpleCppGenerator_cpp_make_var(default_SimpleCppGenerator):
    assert default_SimpleCppGenerator.cpp_make_var(
        'Variable1/Old',
        prefix='pre', suffix='suf', separator='_'
    ) == 'pre_Variable1_Old_suf'


def test_SimpleCppGenerator_cpp_main(default_SimpleCppGenerator):
    assert default_SimpleCppGenerator.cpp_main('body') == \
        '''
int main(int, char** argv) {
  body
  return 0;
}'''


def test_SimpleCppGenerator_cpp_TTree(default_SimpleCppGenerator):
    assert default_SimpleCppGenerator.cpp_TTree('tree', 'tree') == \
        'TTree tree("tree", "tree");\n'


def test_SimpleCppGenerator_cpp_TTreeReader(default_SimpleCppGenerator):
    assert default_SimpleCppGenerator.cpp_TTreeReader(
        'reader', 'tree', 'input_file') == \
        'TTreeReader reader("tree", input_file);\n'


def test_SimpleCppGenerator_cpp_TTreeReaderValue(default_SimpleCppGenerator):
    assert default_SimpleCppGenerator.cpp_TTreeReaderValue(
        'float', 'value', 'reader', 'some_branch') == \
        'TTreeReaderValue<float> value(reader, "some_branch");\n'


##############
# Base maker #
##############

class SimpleMaker(BaseMaker):
    def parse_config(self, filename):
        pass

    def gen(self, filename):
        pass


@pytest.fixture
def default_SimpleMaker():
    return SimpleMaker()


def test_SimpleMaker_read(default_SimpleMaker):
    result = default_SimpleMaker.read(SAMPLE_YAML)
    assert result['YetAnotherTuple']['drop'] == ['Y_OWNPV_COV_', 'Y_OWNPV_P.*']


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
