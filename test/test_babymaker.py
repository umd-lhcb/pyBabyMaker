#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Wed Sep 04, 2019 at 02:22 PM -0400

import pytest
import os
import yaml

from pyBabyMaker.babymaker import BabyCppGenerator

from pyBabyMaker.io.NestedYAMLLoader import NestedYAMLLoader
from pyBabyMaker.io.TupleDump import PyTupleDump
from pyBabyMaker.base import BaseConfigParser
from pyBabyMaker.base import CppCodeDataStore, Variable


SAMPLE_YAML = os.path.join('samples', 'sample-ntuple_process.yml')
SAMPLE_ROOT = os.path.join('samples', 'sample.root')


@pytest.fixture
def load_files():
    print(SAMPLE_YAML)
    with open(SAMPLE_YAML) as f:
        parsed_config = yaml.load(f, NestedYAMLLoader)
    dumped_ntuple = PyTupleDump(SAMPLE_ROOT).dump()
    return (parsed_config, dumped_ntuple)


@pytest.fixture
def default_BabyCppGenerator():
    return BabyCppGenerator(list())


@pytest.fixture
def realistic_BabyCppGenerator(load_files):
    config_parser = BaseConfigParser(*load_files)
    config_parser.parse()
    return BabyCppGenerator(
        config_parser.instructions,
        additional_system_headers=config_parser.additional_system_headers,
        additional_user_headers=config_parser.additional_user_headers
    )


def test_default_BabyCppGenerator(default_BabyCppGenerator):
    data_store = CppCodeDataStore(
        input_file='input.root',
        output_file='output.root',
        input_tree='tree_in',
        output_tree='tree_out',
        selection='Y_PT > 1',
        input_br=[Variable('float', 'Y_PT')],
        output_br=[Variable('float', 'y_pt', 'Y_PT+temp')],
        transient=[Variable('float', 'temp', '1')]
    )
    result = default_BabyCppGenerator.gen_preamble_single_output_tree(
        data_store
    )
    assert result == \
        '''
void generator_tree_out(TFile *input_file, TFile *output_file) {
  TTreeReader reader("tree_in", input_file);

  TTree output("tree_out", "tree_out");


  TTreeReaderValue<float> Y_PT(reader, "Y_PT");

  float y_pt_out;
output.Branch("y_pt", &y_pt_out);


  while (reader.Next()) {
    float temp = 1;

    if ((*Y_PT) > 1) {
  y_pt_out = (*Y_PT)+temp;

  output.Fill();
}
  }

  output_file->Write();
}'''
