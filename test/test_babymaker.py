#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Mon Sep 09, 2019 at 12:08 AM -0400

import pytest
import os

from tempfile import NamedTemporaryFile

from pyBabyMaker.babymaker import BabyCppGenerator
from pyBabyMaker.babymaker import BabyMaker

from pyBabyMaker.base import CppCodeDataStore, Variable


PWD = os.path.dirname(os.path.realpath(__file__))
PARDIR = os.path.join(PWD, os.pardir)
SAMPLE_YAML = os.path.join(PARDIR, 'samples', 'sample-babymaker.yml')
SAMPLE_ROOT = os.path.join(PARDIR, 'samples', 'sample.root')
SAMPLE_CPP = os.path.join(PARDIR, 'samples', 'sample_cpp',
                          'sample-babymaker.cpp')


@pytest.fixture
def default_BabyCppGenerator():
    return BabyCppGenerator(list())


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
}
'''


def test_BabyMaker():
    maker = BabyMaker(SAMPLE_YAML, SAMPLE_ROOT, False)

    with open(SAMPLE_CPP, 'r') as f:
        expected = f.read()

    with NamedTemporaryFile() as f:
        maker.gen(f.name, add_timestamp=False)
        with open(f.name, 'r') as t:
            generated = t.read()

    assert expected == generated
