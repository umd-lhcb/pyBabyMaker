// Author: Yipeng Sun <syp at umd dot edu>
// License: BSD 2-clause
// Last Change: Tue Aug 27, 2019 at 03:46 PM -0400

#include <TDirectoryFile.h>
#include <TFile.h>
#include <TKey.h>
#include <TLeaf.h>
#include <TList.h>
#include <TObjArray.h>
#include <TTree.h>
#include <iostream>
#include <memory>
#include <string>

#include "TupleDump.h"

namespace pyBabyMaker {
TupleDump::TupleDump() {}
TupleDump::~TupleDump() {}

void TupleDump::read(std::string filename) {
  this->ntuple = std::make_unique<TFile>(filename.c_str(), "read");
}

std::vector<std::string> TupleDump::trees() {
  auto keys = (this->ntuple)->GetListOfKeys();
  return TupleDump::traverse(keys);
}

std::vector<std::string> TupleDump::branches(std::string tree) {
  std::vector<std::string> result;
  auto t = dynamic_cast<TTree *>(this->ntuple->Get(tree.c_str()));
  auto b_objs = t->GetListOfBranches();

  for (const auto &&b : *b_objs) {
    const std::string branch = b->GetName();
    result.insert(result.end(), branch);
  }

  return result;
}

std::string TupleDump::datatype(std::string tree, std::string branch) {
  std::string result;
  auto t = dynamic_cast<TTree *>(this->ntuple->Get(tree.c_str()));
  auto b = t->GetBranch(branch.c_str());
  auto l_objs = b->GetListOfLeaves();

  for (const auto &&l : *l_objs) {
    result = (dynamic_cast<TLeaf *>(l))->GetTypeName();
    break;  // Assume the branch is filled with the objects of the same type.
  }

  return result;
}

std::vector<std::string> TupleDump::traverse(TList *keys) {
  std::vector<std::string> result;

  for (const auto &&obj : *keys) {
    auto key = dynamic_cast<TKey *>(obj);
    std::string name = key->GetName();
    std::string class_name = key->GetClassName();

    if (class_name.compare("TDirectoryFile") == 0) {
      auto sub_obj = dynamic_cast<TDirectoryFile *>(key->ReadObj());
      std::vector<std::string> sub_result =
          TupleDump::traverse(sub_obj->GetListOfKeys());

      for (auto &&sub_dir : sub_result) {
        result.insert(result.end(), name + "/" + sub_dir);
      }

    } else if (class_name.compare("TTree") == 0) {
      result.insert(result.end(), name);

    } else {
      std::cout << "Unknown datatype: " << class_name << ". Skip." << std::endl;
    }
  }

  return result;
}

}  // namespace pyBabyMaker
