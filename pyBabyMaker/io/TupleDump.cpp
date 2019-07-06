// Author: Yipeng Sun <syp at umd dot edu>
// License: BSD 2-clause
// Last Change: Sat Jul 06, 2019 at 12:31 AM -0400

#include <TDirectoryFile.h>
#include <TFile.h>
#include <TKey.h>
#include <TLeaf.h>
#include <TList.h>
#include <TObjArray.h>
#include <TTree.h>
#include <iostream>
#include <string>

#include "TupleDump.h"

namespace pyBabyMaker {
TupleDump::~TupleDump() { delete this->ntuple; }

void TupleDump::read(std::string filename) {
  this->ntuple = new TFile(filename.c_str(), "read");
}

std::vector<std::string> TupleDump::dump() {
  auto keys = (this->ntuple)->GetListOfKeys();
  return TupleDump::traverse(keys);
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
