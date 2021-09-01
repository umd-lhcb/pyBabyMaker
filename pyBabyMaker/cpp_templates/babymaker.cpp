// {% gendate: %}
// NOTE: This implementation is very naive.

#include <TFile.h>
#include <TTree.h>
#include <TTreeReader.h>
#include <TString.h>

#include <vector>
#include <iostream>

#include <Math/Vector3D.h>
#include <Math/Vector4D.h>
#include <TMath.h>

// System headers
// {% join: (format_list: "#include <{}>", directive.system_headers), "\n" %}

// User headers
// {% join: (format_list: "#include \"{}\"", directive.user_headers), "\n" %}

using namespace std;
using namespace ROOT::Math;

// Generator for each output tree: one tree per file
// {% for tree_out, config in directive.trees->items: %}
void generator_/* {% guard: tree_out %} */(TTree *input_tree, TString output_prefix) {
  cout << "Generating output ntuple: " << /* {% quote: tree_out %} */ << endl;
  auto output_file = new TFile(output_prefix + /* {% quote: tree_out %} */ + ".root", "recreate");
  TTreeReader reader(input_tree);
  TTree output("tree", "tree");

  // Load needed branches from ntuple
  // {% for var in config.input %}
  //   {% format: "TTreeReaderValue<{}> {}(reader, \"{}\");", var.type, var.fname, var.name %}
  // {% endfor %}

  // Define output branches
  // {% for var in config.output %}
  //   {% declare: var.type, var.fname %}
  //   {% format: "output.Branch(\"{}\", &{});", var.name, var.fname %}
  // {% endfor %}

  // Define temporary variables
  // {% for var in config.tmp %}
  //   {% declare: var.type, var.fname %}
  // {% endfor %}

  while (reader.Next()) {
    // Define variables required by selection
    // {% for var in config.pre_sel_vars %}
    //   {% assign: var.fname, (deref_var: var.rval, config.input_br) %}
    // {% endfor %}

    if (/* {% join: (deref_var_list: config.sel, config.input_br), " && " %} */) {
      // Assign values for each output branch in this loop
      // {% for var in config.post_sel_vars %}
      //   {% assign: var.fname, (deref_var: var.rval, config.input_br) %}
      // {% endfor %}

      output.Fill();
    }
  }

  output_file->Write();
  delete output_file;
}

// {% endfor %}

int main(int, char** argv) {
  TString in_prefix  = TString(argv[1]) + "/";
  TString out_prefix = TString(argv[2]) + "/";

  TFile *ntuple = new TFile(in_prefix + /* {% quote: directive.ntuple %} */);
  cout << "The ntuple being worked on is: " << /* {% quote: directive.ntuple %} */
    << endl;

  vector<TFile*> friend_ntuples;
  // {% for friend in directive.friends %}
    friend_ntuples.push_back(new TFile(in_prefix + /* {% quote: friend %} */));
    cout << "Additional friend ntuple: " << /* {% quote: friend %} */ << endl;
  // {% endfor %}

  // Define input trees and container to store associated friend trees
  // {% for tree in directive.input_trees %}
  //   {% format: "auto tree_{} = static_cast<TTree*>(ntuple->Get(\"{}\"));", (guard: tree), tree %}
  //   {% format: "vector<TTree*> friends_{};", (guard: tree) %}
  // {% endfor %}

  // Handle friend trees
  TTree* tmp_tree;
  // {% for tree in directive.input_trees %}
  //   {% for idx, state in enum: directive.tree_relations[tree] %}
  //     {% if state then %}
  //       {% format: "tmp_tree = static_cast<TTree*>(friend_ntuples[{}]->Get(\"{}\"));", idx, tree %}
           tmp_tree->BuildIndex("runNumber", "eventNumber");
  //       {% format: "tree_{}->AddFriend(tmp_tree, \"{}\", true);", (guard: tree), idx %}
           friends_/* {% guard: tree %} */.push_back(tmp_tree);
           cout << "Handling input tree: " << /* {% quote: tree %} */ << endl;
  //     {% endif %}
  //   {% endfor %}
  // {% endfor %}

  // {% for tree_out, prop in directive.trees->items: %}
  //   {% format: "generator_{}(tree_{}, out_prefix);", (guard: tree_out), (guard: prop.input_tree) %}
  // {% endfor %}

  // Cleanups
  cout <<"Cleanups" << endl;
  delete ntuple;
  // {% for tree in directive.input_trees %}
    for (auto tree : friends_/* {% guard: tree %} */) delete tree;
  // {% endfor %}
  for (auto ntp : friend_ntuples) delete ntp;

  return 0;
}
