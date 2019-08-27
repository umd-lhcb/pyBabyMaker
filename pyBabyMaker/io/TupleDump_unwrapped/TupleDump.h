// Author: Yipeng Sun <syp at umd dot edu>
// License: BSD 2-clause
// Last Change: Tue Aug 27, 2019 at 03:46 PM -0400

#ifndef BMAKER_TUPLEDUMP_H_
#define BMAKER_TUPLEDUMP_H_

#include <TFile.h>
#include <TList.h>
#include <memory>
#include <string>
#include <vector>

namespace pyBabyMaker {
class TupleDump {
 public:
  TupleDump();
  ~TupleDump();

  void read(std::string filename);
  std::vector<std::string> trees();
  std::vector<std::string> branches(std::string tree);
  std::string datatype(std::string tree, std::string branch);

 private:
  std::unique_ptr<TFile> ntuple;
  std::vector<std::string> traverse(TList *keys);
};
}  // namespace pyBabyMaker

#endif
