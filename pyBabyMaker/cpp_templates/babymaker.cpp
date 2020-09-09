// {% gendate: %}
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
  // {% for var in config.input_branches %}
  //   {% format: "TTreeReaderValue<{}> {}(reader, \"{}\");", var.type, var.name, var.name %}
  // {% endfor %}

  // Define output branches
  // {% for var in config.output_branches %}
  //   {% format: "{} {}_out;", var.type, var.name %}
  //   {% format: "output.Branch(\"{}\", &{}_out);", var.name, var.name %}
  // {% endfor %}

  while (reader.Next()) {
    // Define all variables in case required by selection
    //
    // Input branches
    //   All input branches are already available via TTreeReaderValue<>
    //   variables.
    //
    // Transient variables (renamed output branches and temp variables)
    // {% for var in config.transient_vars %}
    //   {% format: "{} {} = {};", var.type, var.name, (deref_var: var.rvalue, config.input_branch_names) %}
    // {% endfor %}

    if (/* {% join: (deref_var_list: config.selection, config.input_branch_names), " && " %} */) {
      // Assign values for each output branch in this loop
      // {% for var in config.output_branches %}
      //   {% format: "{}_out = {};", var.name, (deref_var: var.name, config.input_branch_names) %}
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
