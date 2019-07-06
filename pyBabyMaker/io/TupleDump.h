// Author: Yipeng Sun <syp at umd dot edu>
// License: BSD 2-clause
// Last Change: Sat Jul 06, 2019 at 12:31 AM -0400

#ifndef BMAKER_TUPLEDUMP_H_
#define BMAKER_TUPLEDUMP_H_

#include <TFile.h>
#include <TList.h>
#include <string>
#include <vector>

namespace pyBabyMaker {
class TupleDump {
 public:
  TupleDump();
  ~TupleDump();

  void read(std::string filename);
  std::vector<std::string> dump();

 private:
  TFile *ntuple;
  std::vector<std::string> traverse(TList *keys);
};
}  // namespace pyBabyMaker

#endif
