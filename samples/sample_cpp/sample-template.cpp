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
  // {% format: "TTreeReaderValue<{}> {}(reader, \"{}\");", var.type, var.name, var.name  %}
  // {% endfor %}
}

// {% endfor %}
