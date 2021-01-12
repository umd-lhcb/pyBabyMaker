// {% gendate: %}
// NOTE: This implementation is very naive.

#include <TFile.h>
#include <TTree.h>
#include <TTreeReader.h>
#include <TBranch.h>

// System headers
// {% join: (format_list: "#include <{}>", directive.system_headers), "\n" %}

// User headers
// {% join: (format_list: "#include \"{}\"", directive.user_headers), "\n" %}

// Generator for each output tree
// {% for output_tree, config in directive.trees->items: %}
void generator_/* {% output_tree %} */(TFile *input_file, TFile *output_file) {
  TTreeReader reader("/* {% config.input_tree %} */", input_file);
  TTree output(/* {% format: "\"{}\", \"{}\"", output_tree, output_tree %} */);

  // Load needed branches from ntuple
  // {% for var in config.input %}
  //   {% format: "TTreeReaderValue<{}> {}(reader, \"{}\");", var.type, var.fname, var.name %}
  // {% endfor %}

  // Define output branches
  // {% for var in config.output %}
  //   {% format: "{} {};", var.type, var.fname %}
  //   {% format: "output.Branch(\"{}\", &{});", var.name, var.fname %}
  // {% endfor %}

  // Define temporary variables
  // {% for var in config.tmp %}
  //   {% format: "{} {};", var.type, var.fname %}
  // {% endfor %}

  while (reader.Next()) {
    // Define variables required by selection
    // {% for var in config.pre_sel_vars %}
    //   {% format: "{} = {};", var.fname, (deref_var: var.rval, config.input_br) %}
    // {% endfor %}

    if (/* {% join: (deref_var_list: config.sel, config.input_br), " && " %} */) {
      // Assign values for each output branch in this loop
      // {% for var in config.post_sel_vars %}
      //   {% format: "{} = {};", var.fname, (deref_var: var.rval, config.input_br) %}
      // {% endfor %}

      output.Fill();
    }
  }

  output_file->Write();
}

// {% endfor %}

int main(int, char** argv) {
  TFile *input_file = new TFile(argv[1], "read");
  TFile *output_file = new TFile(argv[2], "recreate");

  // {% for output_tree in directive.trees->keys: %}
  generator_/* {% output_tree %} */(input_file, output_file);
  // {% endfor %}

  output_file->Close();

  delete input_file;
  delete output_file;

  return 0;
}
