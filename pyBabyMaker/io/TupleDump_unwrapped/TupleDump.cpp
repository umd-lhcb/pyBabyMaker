// Author: Yipeng Sun <syp at umd dot edu>
// License: BSD 2-clause
// Last Change: Thu Sep 17, 2020 at 01:24 AM +0800

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
  std::vector<std::string> trees;

  for (const auto &&obj : *keys) {
    auto key = dynamic_cast<TKey *>(obj);
    std::string name = key->GetName();
    std::string class_name = key->GetClassName();

    if (class_name.compare("TDirectoryFile") == 0) {
      auto dir = dynamic_cast<TDirectoryFile *>(key->ReadObj());
      auto sub_dirs = TupleDump::traverse(dir->GetListOfKeys());

      for (auto &&sub_obj : sub_dirs) {
        trees.insert(trees.end(), name + "/" + sub_obj);
      }

    } else if (class_name.compare("TTree") == 0)
      trees.insert(trees.end(), name);
  }

  return trees;
}

}  // namespace pyBabyMaker
