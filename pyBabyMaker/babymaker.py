#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Wed Sep 04, 2019 at 05:01 AM -0400

# from pyBabyMaker.base import BaseCppGenerator, BaseConfigParser, BaseMaker
from pyBabyMaker.base import BaseCppGenerator


class BabyCppGenerator(BaseCppGenerator):
    def gen(self):
        pass

    def gen_preamble(self):
        pass

    def gen_body(self):
        pass

    def gen_preamble_single_output_tree(self, data_store):
        input_tree = self.cpp_TTreeReader(
            'reader', data_store.input_tree, 'input_file')
        output_tree = self.cpp_TTree('output', data_store.output_tree)

        input_br = ''.join(
            [self.cpp_TTreeReaderValue(v.type, v.name, 'reader', v.name)
             for v in data_store.input_br])
        output_br = []
        for v in data_store.output_br:
            output_br.append('{} {}_out;\n'.format(v.type, v.name))
            output_br.append('output.Branch({0}, &{0}_out);\n'.format(v.name))
        output_br = ''.join(output_br)

        transient = ''.join(['{} {} = {};\n'.format(v.type, v.name, v.rvalue)
                             for v in data_store.transient])

        output_vars = '\n'.join(['{} {} = {}'.format(
            v.type, v.name, self.deference_variables(
                v.rvalue, data_store.input_br)) for v in data_store.output_br])

        if not data_store.selection:
            loop = '''{output_vars}
output->Fill();'''.format(output_vars=output_vars)
        else:
            # We need to prepend a '*' to dereference the value input branches
            loop = '''if ({selection}) {{
  {output_vars}
  output->Fill();
}}'''.format(output_vars=output_vars,
             selection=self.deference_variables(
                 data_store.selection, data_store.input_br),
             )

        result = '''
void generator_{name}(TFile *input_file, TFile *output_file) {{
  {input_tree}
  {output_tree}

  {input_br}
  {output_br}

  while (reader.Next()) {{
    {transient}
    {loop}
  }}

  output_file->Write();
}}'''.format(name=self.cpp_make_var(data_store.output_tree),
             input_tree=input_tree, output_tree=output_tree,
             input_br=input_br, output_br=output_br,
             transient=transient, loop=loop)

        return result
