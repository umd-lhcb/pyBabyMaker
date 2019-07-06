#ifndef BMAKER_TUPLEDUMP_H_
#define BMAKER_TUPLEDUMP_H_

#include <TFile.h>
#include <TList.h>
#include <string>
#include <vector>

namespace pyBabyMaker {
class TupleDump {
 public:
  TupleDump(std::string filename);
  ~TupleDump();

  std::vector<std::string> dump();

 private:
  TFile *ntuple;
  std::vector<std::string> traverse(TList *keys);
};
}  // namespace pyBabyMaker

#endif
