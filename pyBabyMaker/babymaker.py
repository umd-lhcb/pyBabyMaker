#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Mon Sep 09, 2019 at 12:10 AM -0400

from pyBabyMaker.base import BaseCppGenerator, BaseConfigParser, BaseMaker


class BabyCppGenerator(BaseCppGenerator):
    def gen(self):
        result = ''
        result += self.gen_timestamp()
        result += self.gen_headers()
        result += self.gen_preamble()
        result += self.gen_body()
        return result

    def gen_preamble(self):
        result = ''
        for data_store in self.instructions:
            result += self.gen_preamble_single_output_tree(data_store)
        return result

    def gen_body(self):
        function_calls = ''.join(
            ['generator_{}(input_file, output_file);\n'.format(
                self.cpp_make_var(i.output_tree)
            ) for i in self.instructions]
        )
        body = '''
TFile *input_file = new TFile(argv[1], "read");
TFile *output_file = new TFile(argv[2], "recreate");

{}

output_file->Close();

delete input_file;
delete output_file;
'''.format(function_calls)
        return self.cpp_main(body)

    def gen_preamble_single_output_tree(self, data_store):
        """
        Generate the body of function call for each ``input_tree`` and
        ``output_tree``.
        """
        input_tree = self.cpp_TTreeReader(
            'reader', data_store.input_tree, 'input_file')
        output_tree = self.cpp_TTree('output', data_store.output_tree)

        input_br = ''.join(
            [self.cpp_TTreeReaderValue(v.type, v.name, 'reader', v.name)
             for v in data_store.input_br])
        output_br = []
        for v in data_store.output_br:
            output_br.append('{} {}_out;\n'.format(v.type, v.name))
            output_br.append('output.Branch("{0}", &{0}_out);\n'.format(v.name))
        output_br = ''.join(output_br)

        transient = ''.join(
            ['{} {} = {};\n'.format(
                v.type, v.name, self.dereference_variables(v.rvalue,
                                                           data_store.input_br))
             for v in data_store.transient])

        output_vars = ''.join(['{}_out = {};\n'.format(
            v.name, self.dereference_variables(v.rvalue, data_store.input_br))
            for v in data_store.output_br])

        if not data_store.selection:
            loop = '''{output_vars}
output.Fill();'''.format(output_vars=output_vars)
        else:
            # We need to prepend a '*' to dereference the value input branches
            loop = '''if ({selection}) {{
  {output_vars}
  output.Fill();
}}'''.format(output_vars=output_vars,
             selection=self.dereference_variables(
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
}}
'''.format(name=self.cpp_make_var(data_store.output_tree),
           input_tree=input_tree, output_tree=output_tree,
           input_br=input_br, output_br=output_br,
           transient=transient, loop=loop)

        return result


class BabyMaker(BaseMaker):
    """
    ``babymaker`` class to glue parser and code generator together.
    """
    def __init__(self, config_filename, ntuple_filename, use_reformater=True):
        """
        Initialize with path to YAML file and n-tuple file.
        """
        self.config_filename = config_filename
        self.ntuple_filename = ntuple_filename
        self.use_reformater = use_reformater

    def gen(self, filename, **kwargs):
        parsed_config = self.read(self.config_filename)
        dumped_ntuple = self.dump(self.ntuple_filename)
        parser = self.parse_config(parsed_config, dumped_ntuple)
        generator = BabyCppGenerator(parser.instructions,
                                     parser.system_headers,
                                     parser.user_headers,
                                     **kwargs)
        content = generator.gen()

        with open(filename, 'w') as f:
            f.write(content)
        if self.use_reformater:
            self.reformat(filename)

    def parse_config(self, parsed_config, dumped_ntuple):
        parser = BaseConfigParser(parsed_config, dumped_ntuple)
        parser.parse()
        return parser
