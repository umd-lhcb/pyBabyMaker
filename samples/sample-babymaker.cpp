// NOTE: This implementation is very naive.

#include <TFile.h>
#include <TTree.h>
#include <TTreeReader.h>
#include <TBranch.h>
#include <TString.h>

#include <vector>
#include <iostream>

// System headers
#include <cmath>
#include <iostream>

// User headers


using namespace std;

// Generator for each output tree: one tree per file
void generator_ATuple(TTree *input_tree, TString output_prefix) {
  cout << "Generating output ntuple: " << "ATuple" << endl;
  auto output_file = new TFile(output_prefix + "ATuple" + ".root", "recreate");
  TTreeReader reader(input_tree);
  TTree output("tree", "tree");

  // Load needed branches from ntuple
  TTreeReaderValue<double> raw_Y_ISOLATION_BDT(reader, "Y_ISOLATION_BDT");
  TTreeReaderValue<double> raw_Y_PT(reader, "Y_PT");
  TTreeReaderValue<double> raw_Y_PE(reader, "Y_PE");
  TTreeReaderValue<UInt_t> raw_runNumber(reader, "runNumber");
  TTreeReaderValue<ULong64_t> raw_eventNumber(reader, "eventNumber");
  TTreeReaderValue<ULong64_t> raw_GpsTime(reader, "GpsTime");
  TTreeReaderValue<double> raw_random_pt(reader, "random_pt");
  TTreeReaderValue<double> raw_Y_PX(reader, "Y_PX");
  TTreeReaderValue<double> raw_Y_PY(reader, "Y_PY");
  TTreeReaderValue<double> raw_Y_PZ(reader, "Y_PZ");
  TTreeReaderValue<double> raw_D0_P(reader, "D0_P");

  // Define output branches
  double keep_Y_PE;
  output.Branch("Y_PE", &keep_Y_PE);
  UInt_t keep_runNumber;
  output.Branch("runNumber", &keep_runNumber);
  ULong64_t keep_eventNumber;
  output.Branch("eventNumber", &keep_eventNumber);
  ULong64_t keep_GpsTime;
  output.Branch("GpsTime", &keep_GpsTime);
  double keep_random_pt;
  output.Branch("random_pt", &keep_random_pt);
  double rename_y_pt;
  output.Branch("y_pt", &rename_y_pt);
  double rename_y_px;
  output.Branch("y_px", &rename_y_px);
  double rename_y_py;
  output.Branch("y_py", &rename_y_py);
  double rename_y_pz;
  output.Branch("y_pz", &rename_y_pz);
  double calculation_RandStuff;
  output.Branch("RandStuff", &calculation_RandStuff);
  double calculation_some_other_var;
  output.Branch("some_other_var", &calculation_some_other_var);
  double calculation_alt_def;
  output.Branch("alt_def", &calculation_alt_def);

  // Define temporary variables
  double calculation_TempStuff;
  double calculation_some_var;

  while (reader.Next()) {
    // Define variables required by selection

    if ((true) && ((*raw_Y_ISOLATION_BDT) > 0) && ((*raw_Y_PT) > 10000)) {
      // Assign values for each output branch in this loop
      keep_Y_PE = (*raw_Y_PE);
      keep_runNumber = (*raw_runNumber);
      keep_eventNumber = (*raw_eventNumber);
      keep_GpsTime = (*raw_GpsTime);
      keep_random_pt = (*raw_random_pt);
      rename_y_pt = (*raw_Y_PT);
      rename_y_px = (*raw_Y_PX);
      rename_y_py = (*raw_Y_PY);
      rename_y_pz = (*raw_Y_PZ);
      calculation_TempStuff = (*raw_D0_P)+(*raw_Y_PT);
      calculation_RandStuff = calculation_TempStuff*3.14;
      calculation_some_var = rename_y_pt + rename_y_pz;
      calculation_some_other_var = calculation_some_var*3.14;
      calculation_alt_def = (*raw_Y_PE);

      output.Fill();
    }
  }

  output_file->Write();
  delete output_file;
}

void generator_AnotherTuple(TTree *input_tree, TString output_prefix) {
  cout << "Generating output ntuple: " << "AnotherTuple" << endl;
  auto output_file = new TFile(output_prefix + "AnotherTuple" + ".root", "recreate");
  TTreeReader reader(input_tree);
  TTree output("tree", "tree");

  // Load needed branches from ntuple
  TTreeReaderValue<double> raw_Y_ISOLATION_BDT(reader, "Y_ISOLATION_BDT");
  TTreeReaderValue<double> raw_Y_PT(reader, "Y_PT");
  TTreeReaderValue<double> raw_Y_PE(reader, "Y_PE");
  TTreeReaderValue<double> raw_Y_PX(reader, "Y_PX");
  TTreeReaderValue<double> raw_Y_PY(reader, "Y_PY");
  TTreeReaderValue<double> raw_Y_PZ(reader, "Y_PZ");
  TTreeReaderValue<UInt_t> raw_runNumber(reader, "runNumber");
  TTreeReaderValue<ULong64_t> raw_eventNumber(reader, "eventNumber");
  TTreeReaderValue<ULong64_t> raw_GpsTime(reader, "GpsTime");
  TTreeReaderValue<double> raw_random_pt(reader, "random_pt");
  TTreeReaderValue<double> raw_D0_P(reader, "D0_P");

  // Define output branches
  double rename_b0_pt;
  output.Branch("b0_pt", &rename_b0_pt);
  double keep_Y_PE;
  output.Branch("Y_PE", &keep_Y_PE);
  double keep_Y_PX;
  output.Branch("Y_PX", &keep_Y_PX);
  double keep_Y_PY;
  output.Branch("Y_PY", &keep_Y_PY);
  double keep_Y_PZ;
  output.Branch("Y_PZ", &keep_Y_PZ);
  UInt_t keep_runNumber;
  output.Branch("runNumber", &keep_runNumber);
  ULong64_t keep_eventNumber;
  output.Branch("eventNumber", &keep_eventNumber);
  ULong64_t keep_GpsTime;
  output.Branch("GpsTime", &keep_GpsTime);
  double keep_random_pt;
  output.Branch("random_pt", &keep_random_pt);
  double calculation_RandStuff;
  output.Branch("RandStuff", &calculation_RandStuff);

  // Define temporary variables
  double calculation_TempStuff;

  while (reader.Next()) {
    // Define variables required by selection
    rename_b0_pt = (*raw_Y_PT);

    if ((true) && ((*raw_Y_ISOLATION_BDT) > 0) && (rename_b0_pt > 10000) && ((*raw_Y_PE) > (100 * pow(10, 3)))) {
      // Assign values for each output branch in this loop
      keep_Y_PE = (*raw_Y_PE);
      keep_Y_PX = (*raw_Y_PX);
      keep_Y_PY = (*raw_Y_PY);
      keep_Y_PZ = (*raw_Y_PZ);
      keep_runNumber = (*raw_runNumber);
      keep_eventNumber = (*raw_eventNumber);
      keep_GpsTime = (*raw_GpsTime);
      keep_random_pt = (*raw_random_pt);
      calculation_TempStuff = (*raw_D0_P)+(*raw_Y_PT);
      calculation_RandStuff = calculation_TempStuff*3.14;

      output.Fill();
    }
  }

  output_file->Write();
  delete output_file;
}

void generator_YetAnotherTuple(TTree *input_tree, TString output_prefix) {
  cout << "Generating output ntuple: " << "YetAnotherTuple" << endl;
  auto output_file = new TFile(output_prefix + "YetAnotherTuple" + ".root", "recreate");
  TTreeReader reader(input_tree);
  TTree output("tree", "tree");

  // Load needed branches from ntuple
  TTreeReaderValue<double> raw_Y_ISOLATION_BDT(reader, "Y_ISOLATION_BDT");
  TTreeReaderValue<bool> raw_piminus_isMuon(reader, "piminus_isMuon");
  TTreeReaderValue<double> raw_Y_OWNPV_X(reader, "Y_OWNPV_X");
  TTreeReaderValue<double> raw_Y_OWNPV_Y(reader, "Y_OWNPV_Y");
  TTreeReaderValue<double> raw_Y_OWNPV_Z(reader, "Y_OWNPV_Z");
  TTreeReaderValue<double> raw_Y_OWNPV_XERR(reader, "Y_OWNPV_XERR");
  TTreeReaderValue<double> raw_Y_OWNPV_YERR(reader, "Y_OWNPV_YERR");
  TTreeReaderValue<double> raw_Y_OWNPV_ZERR(reader, "Y_OWNPV_ZERR");
  TTreeReaderValue<double> raw_Y_OWNPV_CHI2(reader, "Y_OWNPV_CHI2");
  TTreeReaderValue<int32_t> raw_Y_OWNPV_NDOF(reader, "Y_OWNPV_NDOF");
  TTreeReaderValue<double> raw_Y_PE(reader, "Y_PE");
  TTreeReaderValue<double> raw_Y_ISOLATION_CHI2(reader, "Y_ISOLATION_CHI2");
  TTreeReaderValue<double> raw_Y_ISOLATION_ANGLE(reader, "Y_ISOLATION_ANGLE");
  TTreeReaderValue<int32_t> raw_Y_ISOLATION_SC(reader, "Y_ISOLATION_SC");
  TTreeReaderValue<float> raw_Y_ISOLATION_CHARGE(reader, "Y_ISOLATION_CHARGE");
  TTreeReaderValue<float> raw_Y_ISOLATION_Type(reader, "Y_ISOLATION_Type");
  TTreeReaderValue<float> raw_Y_ISOLATION_PE(reader, "Y_ISOLATION_PE");
  TTreeReaderValue<float> raw_Y_ISOLATION_PX(reader, "Y_ISOLATION_PX");
  TTreeReaderValue<float> raw_Y_ISOLATION_PY(reader, "Y_ISOLATION_PY");
  TTreeReaderValue<float> raw_Y_ISOLATION_PZ(reader, "Y_ISOLATION_PZ");
  TTreeReaderValue<float> raw_Y_ISOLATION_PIDK(reader, "Y_ISOLATION_PIDK");
  TTreeReaderValue<float> raw_Y_ISOLATION_PIDp(reader, "Y_ISOLATION_PIDp");
  TTreeReaderValue<float> raw_Y_ISOLATION_NNk(reader, "Y_ISOLATION_NNk");
  TTreeReaderValue<float> raw_Y_ISOLATION_NNpi(reader, "Y_ISOLATION_NNpi");
  TTreeReaderValue<float> raw_Y_ISOLATION_NNp(reader, "Y_ISOLATION_NNp");
  TTreeReaderValue<float> raw_Y_ISOLATION_IsMuon(reader, "Y_ISOLATION_IsMuon");
  TTreeReaderValue<float> raw_Y_ISOLATION_NNghost(reader, "Y_ISOLATION_NNghost");
  TTreeReaderValue<int32_t> raw_Y_ISOLATION_TRUEID(reader, "Y_ISOLATION_TRUEID");
  TTreeReaderValue<double> raw_Y_ISOLATION_CHI22(reader, "Y_ISOLATION_CHI22");
  TTreeReaderValue<int32_t> raw_Y_ISOLATION_SC2(reader, "Y_ISOLATION_SC2");
  TTreeReaderValue<double> raw_Y_ISOLATION_ANGLE2(reader, "Y_ISOLATION_ANGLE2");
  TTreeReaderValue<double> raw_Y_ISOLATION_BDT2(reader, "Y_ISOLATION_BDT2");
  TTreeReaderValue<float> raw_Y_ISOLATION_CHARGE2(reader, "Y_ISOLATION_CHARGE2");
  TTreeReaderValue<float> raw_Y_ISOLATION_Type2(reader, "Y_ISOLATION_Type2");
  TTreeReaderValue<float> raw_Y_ISOLATION_PE2(reader, "Y_ISOLATION_PE2");
  TTreeReaderValue<float> raw_Y_ISOLATION_PX2(reader, "Y_ISOLATION_PX2");
  TTreeReaderValue<float> raw_Y_ISOLATION_PY2(reader, "Y_ISOLATION_PY2");
  TTreeReaderValue<float> raw_Y_ISOLATION_PZ2(reader, "Y_ISOLATION_PZ2");
  TTreeReaderValue<float> raw_Y_ISOLATION_PIDK2(reader, "Y_ISOLATION_PIDK2");
  TTreeReaderValue<float> raw_Y_ISOLATION_PIDp2(reader, "Y_ISOLATION_PIDp2");
  TTreeReaderValue<float> raw_Y_ISOLATION_NNk2(reader, "Y_ISOLATION_NNk2");
  TTreeReaderValue<float> raw_Y_ISOLATION_NNpi2(reader, "Y_ISOLATION_NNpi2");
  TTreeReaderValue<float> raw_Y_ISOLATION_NNp2(reader, "Y_ISOLATION_NNp2");
  TTreeReaderValue<float> raw_Y_ISOLATION_IsMuon2(reader, "Y_ISOLATION_IsMuon2");
  TTreeReaderValue<float> raw_Y_ISOLATION_NNghost2(reader, "Y_ISOLATION_NNghost2");
  TTreeReaderValue<int32_t> raw_Y_ISOLATION_TRUEID2(reader, "Y_ISOLATION_TRUEID2");
  TTreeReaderValue<double> raw_Y_ISOLATION_CHI23(reader, "Y_ISOLATION_CHI23");
  TTreeReaderValue<int32_t> raw_Y_ISOLATION_SC3(reader, "Y_ISOLATION_SC3");
  TTreeReaderValue<double> raw_Y_ISOLATION_BDT3(reader, "Y_ISOLATION_BDT3");
  TTreeReaderValue<double> raw_Y_ISOLATION_ANGLE3(reader, "Y_ISOLATION_ANGLE3");
  TTreeReaderValue<float> raw_Y_ISOLATION_CHARGE3(reader, "Y_ISOLATION_CHARGE3");
  TTreeReaderValue<float> raw_Y_ISOLATION_Type3(reader, "Y_ISOLATION_Type3");
  TTreeReaderValue<float> raw_Y_ISOLATION_PE3(reader, "Y_ISOLATION_PE3");
  TTreeReaderValue<float> raw_Y_ISOLATION_PX3(reader, "Y_ISOLATION_PX3");
  TTreeReaderValue<float> raw_Y_ISOLATION_PY3(reader, "Y_ISOLATION_PY3");
  TTreeReaderValue<float> raw_Y_ISOLATION_PZ3(reader, "Y_ISOLATION_PZ3");
  TTreeReaderValue<float> raw_Y_ISOLATION_PIDK3(reader, "Y_ISOLATION_PIDK3");
  TTreeReaderValue<float> raw_Y_ISOLATION_PIDp3(reader, "Y_ISOLATION_PIDp3");
  TTreeReaderValue<float> raw_Y_ISOLATION_NNk3(reader, "Y_ISOLATION_NNk3");
  TTreeReaderValue<float> raw_Y_ISOLATION_NNpi3(reader, "Y_ISOLATION_NNpi3");
  TTreeReaderValue<float> raw_Y_ISOLATION_NNp3(reader, "Y_ISOLATION_NNp3");
  TTreeReaderValue<float> raw_Y_ISOLATION_IsMuon3(reader, "Y_ISOLATION_IsMuon3");
  TTreeReaderValue<float> raw_Y_ISOLATION_NNghost3(reader, "Y_ISOLATION_NNghost3");
  TTreeReaderValue<int32_t> raw_Y_ISOLATION_TRUEID3(reader, "Y_ISOLATION_TRUEID3");
  TTreeReaderValue<double> raw_Y_ISOLATION_CHI24(reader, "Y_ISOLATION_CHI24");
  TTreeReaderValue<int32_t> raw_Y_ISOLATION_SC4(reader, "Y_ISOLATION_SC4");
  TTreeReaderValue<double> raw_Y_ISOLATION_BDT4(reader, "Y_ISOLATION_BDT4");
  TTreeReaderValue<double> raw_Y_ISOLATION_ANGLE4(reader, "Y_ISOLATION_ANGLE4");
  TTreeReaderValue<float> raw_Y_ISOLATION_CHARGE4(reader, "Y_ISOLATION_CHARGE4");
  TTreeReaderValue<float> raw_Y_ISOLATION_Type4(reader, "Y_ISOLATION_Type4");
  TTreeReaderValue<float> raw_Y_ISOLATION_PE4(reader, "Y_ISOLATION_PE4");
  TTreeReaderValue<float> raw_Y_ISOLATION_PX4(reader, "Y_ISOLATION_PX4");
  TTreeReaderValue<float> raw_Y_ISOLATION_PY4(reader, "Y_ISOLATION_PY4");
  TTreeReaderValue<float> raw_Y_ISOLATION_PZ4(reader, "Y_ISOLATION_PZ4");
  TTreeReaderValue<float> raw_Y_ISOLATION_PIDK4(reader, "Y_ISOLATION_PIDK4");
  TTreeReaderValue<float> raw_Y_ISOLATION_PIDp4(reader, "Y_ISOLATION_PIDp4");
  TTreeReaderValue<float> raw_Y_ISOLATION_NNk4(reader, "Y_ISOLATION_NNk4");
  TTreeReaderValue<float> raw_Y_ISOLATION_NNpi4(reader, "Y_ISOLATION_NNpi4");
  TTreeReaderValue<float> raw_Y_ISOLATION_NNp4(reader, "Y_ISOLATION_NNp4");
  TTreeReaderValue<float> raw_Y_ISOLATION_IsMuon4(reader, "Y_ISOLATION_IsMuon4");
  TTreeReaderValue<float> raw_Y_ISOLATION_NNghost4(reader, "Y_ISOLATION_NNghost4");
  TTreeReaderValue<int32_t> raw_Y_ISOLATION_TRUEID4(reader, "Y_ISOLATION_TRUEID4");
  TTreeReaderValue<UInt_t> raw_runNumber(reader, "runNumber");
  TTreeReaderValue<ULong64_t> raw_eventNumber(reader, "eventNumber");
  TTreeReaderValue<ULong64_t> raw_GpsTime(reader, "GpsTime");
  TTreeReaderValue<double> raw_Y_PT(reader, "Y_PT");
  TTreeReaderValue<double> raw_Y_PX(reader, "Y_PX");
  TTreeReaderValue<double> raw_Y_PY(reader, "Y_PY");
  TTreeReaderValue<double> raw_Y_PZ(reader, "Y_PZ");
  TTreeReaderValue<double> raw_D0_P(reader, "D0_P");

  // Define output branches
  double keep_Y_OWNPV_X;
  output.Branch("Y_OWNPV_X", &keep_Y_OWNPV_X);
  double keep_Y_OWNPV_Y;
  output.Branch("Y_OWNPV_Y", &keep_Y_OWNPV_Y);
  double keep_Y_OWNPV_Z;
  output.Branch("Y_OWNPV_Z", &keep_Y_OWNPV_Z);
  double keep_Y_OWNPV_XERR;
  output.Branch("Y_OWNPV_XERR", &keep_Y_OWNPV_XERR);
  double keep_Y_OWNPV_YERR;
  output.Branch("Y_OWNPV_YERR", &keep_Y_OWNPV_YERR);
  double keep_Y_OWNPV_ZERR;
  output.Branch("Y_OWNPV_ZERR", &keep_Y_OWNPV_ZERR);
  double keep_Y_OWNPV_CHI2;
  output.Branch("Y_OWNPV_CHI2", &keep_Y_OWNPV_CHI2);
  int32_t keep_Y_OWNPV_NDOF;
  output.Branch("Y_OWNPV_NDOF", &keep_Y_OWNPV_NDOF);
  double keep_Y_PE;
  output.Branch("Y_PE", &keep_Y_PE);
  double keep_Y_ISOLATION_CHI2;
  output.Branch("Y_ISOLATION_CHI2", &keep_Y_ISOLATION_CHI2);
  double keep_Y_ISOLATION_ANGLE;
  output.Branch("Y_ISOLATION_ANGLE", &keep_Y_ISOLATION_ANGLE);
  int32_t keep_Y_ISOLATION_SC;
  output.Branch("Y_ISOLATION_SC", &keep_Y_ISOLATION_SC);
  double keep_Y_ISOLATION_BDT;
  output.Branch("Y_ISOLATION_BDT", &keep_Y_ISOLATION_BDT);
  float keep_Y_ISOLATION_CHARGE;
  output.Branch("Y_ISOLATION_CHARGE", &keep_Y_ISOLATION_CHARGE);
  float keep_Y_ISOLATION_Type;
  output.Branch("Y_ISOLATION_Type", &keep_Y_ISOLATION_Type);
  float keep_Y_ISOLATION_PE;
  output.Branch("Y_ISOLATION_PE", &keep_Y_ISOLATION_PE);
  float keep_Y_ISOLATION_PX;
  output.Branch("Y_ISOLATION_PX", &keep_Y_ISOLATION_PX);
  float keep_Y_ISOLATION_PY;
  output.Branch("Y_ISOLATION_PY", &keep_Y_ISOLATION_PY);
  float keep_Y_ISOLATION_PZ;
  output.Branch("Y_ISOLATION_PZ", &keep_Y_ISOLATION_PZ);
  float keep_Y_ISOLATION_PIDK;
  output.Branch("Y_ISOLATION_PIDK", &keep_Y_ISOLATION_PIDK);
  float keep_Y_ISOLATION_PIDp;
  output.Branch("Y_ISOLATION_PIDp", &keep_Y_ISOLATION_PIDp);
  float keep_Y_ISOLATION_NNk;
  output.Branch("Y_ISOLATION_NNk", &keep_Y_ISOLATION_NNk);
  float keep_Y_ISOLATION_NNpi;
  output.Branch("Y_ISOLATION_NNpi", &keep_Y_ISOLATION_NNpi);
  float keep_Y_ISOLATION_NNp;
  output.Branch("Y_ISOLATION_NNp", &keep_Y_ISOLATION_NNp);
  float keep_Y_ISOLATION_IsMuon;
  output.Branch("Y_ISOLATION_IsMuon", &keep_Y_ISOLATION_IsMuon);
  float keep_Y_ISOLATION_NNghost;
  output.Branch("Y_ISOLATION_NNghost", &keep_Y_ISOLATION_NNghost);
  int32_t keep_Y_ISOLATION_TRUEID;
  output.Branch("Y_ISOLATION_TRUEID", &keep_Y_ISOLATION_TRUEID);
  double keep_Y_ISOLATION_CHI22;
  output.Branch("Y_ISOLATION_CHI22", &keep_Y_ISOLATION_CHI22);
  int32_t keep_Y_ISOLATION_SC2;
  output.Branch("Y_ISOLATION_SC2", &keep_Y_ISOLATION_SC2);
  double keep_Y_ISOLATION_ANGLE2;
  output.Branch("Y_ISOLATION_ANGLE2", &keep_Y_ISOLATION_ANGLE2);
  double keep_Y_ISOLATION_BDT2;
  output.Branch("Y_ISOLATION_BDT2", &keep_Y_ISOLATION_BDT2);
  float keep_Y_ISOLATION_CHARGE2;
  output.Branch("Y_ISOLATION_CHARGE2", &keep_Y_ISOLATION_CHARGE2);
  float keep_Y_ISOLATION_Type2;
  output.Branch("Y_ISOLATION_Type2", &keep_Y_ISOLATION_Type2);
  float keep_Y_ISOLATION_PE2;
  output.Branch("Y_ISOLATION_PE2", &keep_Y_ISOLATION_PE2);
  float keep_Y_ISOLATION_PX2;
  output.Branch("Y_ISOLATION_PX2", &keep_Y_ISOLATION_PX2);
  float keep_Y_ISOLATION_PY2;
  output.Branch("Y_ISOLATION_PY2", &keep_Y_ISOLATION_PY2);
  float keep_Y_ISOLATION_PZ2;
  output.Branch("Y_ISOLATION_PZ2", &keep_Y_ISOLATION_PZ2);
  float keep_Y_ISOLATION_PIDK2;
  output.Branch("Y_ISOLATION_PIDK2", &keep_Y_ISOLATION_PIDK2);
  float keep_Y_ISOLATION_PIDp2;
  output.Branch("Y_ISOLATION_PIDp2", &keep_Y_ISOLATION_PIDp2);
  float keep_Y_ISOLATION_NNk2;
  output.Branch("Y_ISOLATION_NNk2", &keep_Y_ISOLATION_NNk2);
  float keep_Y_ISOLATION_NNpi2;
  output.Branch("Y_ISOLATION_NNpi2", &keep_Y_ISOLATION_NNpi2);
  float keep_Y_ISOLATION_NNp2;
  output.Branch("Y_ISOLATION_NNp2", &keep_Y_ISOLATION_NNp2);
  float keep_Y_ISOLATION_IsMuon2;
  output.Branch("Y_ISOLATION_IsMuon2", &keep_Y_ISOLATION_IsMuon2);
  float keep_Y_ISOLATION_NNghost2;
  output.Branch("Y_ISOLATION_NNghost2", &keep_Y_ISOLATION_NNghost2);
  int32_t keep_Y_ISOLATION_TRUEID2;
  output.Branch("Y_ISOLATION_TRUEID2", &keep_Y_ISOLATION_TRUEID2);
  double keep_Y_ISOLATION_CHI23;
  output.Branch("Y_ISOLATION_CHI23", &keep_Y_ISOLATION_CHI23);
  int32_t keep_Y_ISOLATION_SC3;
  output.Branch("Y_ISOLATION_SC3", &keep_Y_ISOLATION_SC3);
  double keep_Y_ISOLATION_BDT3;
  output.Branch("Y_ISOLATION_BDT3", &keep_Y_ISOLATION_BDT3);
  double keep_Y_ISOLATION_ANGLE3;
  output.Branch("Y_ISOLATION_ANGLE3", &keep_Y_ISOLATION_ANGLE3);
  float keep_Y_ISOLATION_CHARGE3;
  output.Branch("Y_ISOLATION_CHARGE3", &keep_Y_ISOLATION_CHARGE3);
  float keep_Y_ISOLATION_Type3;
  output.Branch("Y_ISOLATION_Type3", &keep_Y_ISOLATION_Type3);
  float keep_Y_ISOLATION_PE3;
  output.Branch("Y_ISOLATION_PE3", &keep_Y_ISOLATION_PE3);
  float keep_Y_ISOLATION_PX3;
  output.Branch("Y_ISOLATION_PX3", &keep_Y_ISOLATION_PX3);
  float keep_Y_ISOLATION_PY3;
  output.Branch("Y_ISOLATION_PY3", &keep_Y_ISOLATION_PY3);
  float keep_Y_ISOLATION_PZ3;
  output.Branch("Y_ISOLATION_PZ3", &keep_Y_ISOLATION_PZ3);
  float keep_Y_ISOLATION_PIDK3;
  output.Branch("Y_ISOLATION_PIDK3", &keep_Y_ISOLATION_PIDK3);
  float keep_Y_ISOLATION_PIDp3;
  output.Branch("Y_ISOLATION_PIDp3", &keep_Y_ISOLATION_PIDp3);
  float keep_Y_ISOLATION_NNk3;
  output.Branch("Y_ISOLATION_NNk3", &keep_Y_ISOLATION_NNk3);
  float keep_Y_ISOLATION_NNpi3;
  output.Branch("Y_ISOLATION_NNpi3", &keep_Y_ISOLATION_NNpi3);
  float keep_Y_ISOLATION_NNp3;
  output.Branch("Y_ISOLATION_NNp3", &keep_Y_ISOLATION_NNp3);
  float keep_Y_ISOLATION_IsMuon3;
  output.Branch("Y_ISOLATION_IsMuon3", &keep_Y_ISOLATION_IsMuon3);
  float keep_Y_ISOLATION_NNghost3;
  output.Branch("Y_ISOLATION_NNghost3", &keep_Y_ISOLATION_NNghost3);
  int32_t keep_Y_ISOLATION_TRUEID3;
  output.Branch("Y_ISOLATION_TRUEID3", &keep_Y_ISOLATION_TRUEID3);
  double keep_Y_ISOLATION_CHI24;
  output.Branch("Y_ISOLATION_CHI24", &keep_Y_ISOLATION_CHI24);
  int32_t keep_Y_ISOLATION_SC4;
  output.Branch("Y_ISOLATION_SC4", &keep_Y_ISOLATION_SC4);
  double keep_Y_ISOLATION_BDT4;
  output.Branch("Y_ISOLATION_BDT4", &keep_Y_ISOLATION_BDT4);
  double keep_Y_ISOLATION_ANGLE4;
  output.Branch("Y_ISOLATION_ANGLE4", &keep_Y_ISOLATION_ANGLE4);
  float keep_Y_ISOLATION_CHARGE4;
  output.Branch("Y_ISOLATION_CHARGE4", &keep_Y_ISOLATION_CHARGE4);
  float keep_Y_ISOLATION_Type4;
  output.Branch("Y_ISOLATION_Type4", &keep_Y_ISOLATION_Type4);
  float keep_Y_ISOLATION_PE4;
  output.Branch("Y_ISOLATION_PE4", &keep_Y_ISOLATION_PE4);
  float keep_Y_ISOLATION_PX4;
  output.Branch("Y_ISOLATION_PX4", &keep_Y_ISOLATION_PX4);
  float keep_Y_ISOLATION_PY4;
  output.Branch("Y_ISOLATION_PY4", &keep_Y_ISOLATION_PY4);
  float keep_Y_ISOLATION_PZ4;
  output.Branch("Y_ISOLATION_PZ4", &keep_Y_ISOLATION_PZ4);
  float keep_Y_ISOLATION_PIDK4;
  output.Branch("Y_ISOLATION_PIDK4", &keep_Y_ISOLATION_PIDK4);
  float keep_Y_ISOLATION_PIDp4;
  output.Branch("Y_ISOLATION_PIDp4", &keep_Y_ISOLATION_PIDp4);
  float keep_Y_ISOLATION_NNk4;
  output.Branch("Y_ISOLATION_NNk4", &keep_Y_ISOLATION_NNk4);
  float keep_Y_ISOLATION_NNpi4;
  output.Branch("Y_ISOLATION_NNpi4", &keep_Y_ISOLATION_NNpi4);
  float keep_Y_ISOLATION_NNp4;
  output.Branch("Y_ISOLATION_NNp4", &keep_Y_ISOLATION_NNp4);
  float keep_Y_ISOLATION_IsMuon4;
  output.Branch("Y_ISOLATION_IsMuon4", &keep_Y_ISOLATION_IsMuon4);
  float keep_Y_ISOLATION_NNghost4;
  output.Branch("Y_ISOLATION_NNghost4", &keep_Y_ISOLATION_NNghost4);
  int32_t keep_Y_ISOLATION_TRUEID4;
  output.Branch("Y_ISOLATION_TRUEID4", &keep_Y_ISOLATION_TRUEID4);
  UInt_t keep_runNumber;
  output.Branch("runNumber", &keep_runNumber);
  ULong64_t keep_eventNumber;
  output.Branch("eventNumber", &keep_eventNumber);
  ULong64_t keep_GpsTime;
  output.Branch("GpsTime", &keep_GpsTime);
  double rename_y_pt;
  output.Branch("y_pt", &rename_y_pt);
  double rename_y_px;
  output.Branch("y_px", &rename_y_px);
  double rename_y_py;
  output.Branch("y_py", &rename_y_py);
  double rename_y_pz;
  output.Branch("y_pz", &rename_y_pz);
  double calculation_RandStuff;
  output.Branch("RandStuff", &calculation_RandStuff);
  double calculation_some_other_var;
  output.Branch("some_other_var", &calculation_some_other_var);

  // Define temporary variables
  double calculation_TempStuff;
  double calculation_some_var;

  while (reader.Next()) {
    // Define variables required by selection

    if ((true) && ((*raw_Y_ISOLATION_BDT) > 0) && ((*raw_piminus_isMuon))) {
      // Assign values for each output branch in this loop
      keep_Y_OWNPV_X = (*raw_Y_OWNPV_X);
      keep_Y_OWNPV_Y = (*raw_Y_OWNPV_Y);
      keep_Y_OWNPV_Z = (*raw_Y_OWNPV_Z);
      keep_Y_OWNPV_XERR = (*raw_Y_OWNPV_XERR);
      keep_Y_OWNPV_YERR = (*raw_Y_OWNPV_YERR);
      keep_Y_OWNPV_ZERR = (*raw_Y_OWNPV_ZERR);
      keep_Y_OWNPV_CHI2 = (*raw_Y_OWNPV_CHI2);
      keep_Y_OWNPV_NDOF = (*raw_Y_OWNPV_NDOF);
      keep_Y_PE = (*raw_Y_PE);
      keep_Y_ISOLATION_CHI2 = (*raw_Y_ISOLATION_CHI2);
      keep_Y_ISOLATION_ANGLE = (*raw_Y_ISOLATION_ANGLE);
      keep_Y_ISOLATION_SC = (*raw_Y_ISOLATION_SC);
      keep_Y_ISOLATION_BDT = (*raw_Y_ISOLATION_BDT);
      keep_Y_ISOLATION_CHARGE = (*raw_Y_ISOLATION_CHARGE);
      keep_Y_ISOLATION_Type = (*raw_Y_ISOLATION_Type);
      keep_Y_ISOLATION_PE = (*raw_Y_ISOLATION_PE);
      keep_Y_ISOLATION_PX = (*raw_Y_ISOLATION_PX);
      keep_Y_ISOLATION_PY = (*raw_Y_ISOLATION_PY);
      keep_Y_ISOLATION_PZ = (*raw_Y_ISOLATION_PZ);
      keep_Y_ISOLATION_PIDK = (*raw_Y_ISOLATION_PIDK);
      keep_Y_ISOLATION_PIDp = (*raw_Y_ISOLATION_PIDp);
      keep_Y_ISOLATION_NNk = (*raw_Y_ISOLATION_NNk);
      keep_Y_ISOLATION_NNpi = (*raw_Y_ISOLATION_NNpi);
      keep_Y_ISOLATION_NNp = (*raw_Y_ISOLATION_NNp);
      keep_Y_ISOLATION_IsMuon = (*raw_Y_ISOLATION_IsMuon);
      keep_Y_ISOLATION_NNghost = (*raw_Y_ISOLATION_NNghost);
      keep_Y_ISOLATION_TRUEID = (*raw_Y_ISOLATION_TRUEID);
      keep_Y_ISOLATION_CHI22 = (*raw_Y_ISOLATION_CHI22);
      keep_Y_ISOLATION_SC2 = (*raw_Y_ISOLATION_SC2);
      keep_Y_ISOLATION_ANGLE2 = (*raw_Y_ISOLATION_ANGLE2);
      keep_Y_ISOLATION_BDT2 = (*raw_Y_ISOLATION_BDT2);
      keep_Y_ISOLATION_CHARGE2 = (*raw_Y_ISOLATION_CHARGE2);
      keep_Y_ISOLATION_Type2 = (*raw_Y_ISOLATION_Type2);
      keep_Y_ISOLATION_PE2 = (*raw_Y_ISOLATION_PE2);
      keep_Y_ISOLATION_PX2 = (*raw_Y_ISOLATION_PX2);
      keep_Y_ISOLATION_PY2 = (*raw_Y_ISOLATION_PY2);
      keep_Y_ISOLATION_PZ2 = (*raw_Y_ISOLATION_PZ2);
      keep_Y_ISOLATION_PIDK2 = (*raw_Y_ISOLATION_PIDK2);
      keep_Y_ISOLATION_PIDp2 = (*raw_Y_ISOLATION_PIDp2);
      keep_Y_ISOLATION_NNk2 = (*raw_Y_ISOLATION_NNk2);
      keep_Y_ISOLATION_NNpi2 = (*raw_Y_ISOLATION_NNpi2);
      keep_Y_ISOLATION_NNp2 = (*raw_Y_ISOLATION_NNp2);
      keep_Y_ISOLATION_IsMuon2 = (*raw_Y_ISOLATION_IsMuon2);
      keep_Y_ISOLATION_NNghost2 = (*raw_Y_ISOLATION_NNghost2);
      keep_Y_ISOLATION_TRUEID2 = (*raw_Y_ISOLATION_TRUEID2);
      keep_Y_ISOLATION_CHI23 = (*raw_Y_ISOLATION_CHI23);
      keep_Y_ISOLATION_SC3 = (*raw_Y_ISOLATION_SC3);
      keep_Y_ISOLATION_BDT3 = (*raw_Y_ISOLATION_BDT3);
      keep_Y_ISOLATION_ANGLE3 = (*raw_Y_ISOLATION_ANGLE3);
      keep_Y_ISOLATION_CHARGE3 = (*raw_Y_ISOLATION_CHARGE3);
      keep_Y_ISOLATION_Type3 = (*raw_Y_ISOLATION_Type3);
      keep_Y_ISOLATION_PE3 = (*raw_Y_ISOLATION_PE3);
      keep_Y_ISOLATION_PX3 = (*raw_Y_ISOLATION_PX3);
      keep_Y_ISOLATION_PY3 = (*raw_Y_ISOLATION_PY3);
      keep_Y_ISOLATION_PZ3 = (*raw_Y_ISOLATION_PZ3);
      keep_Y_ISOLATION_PIDK3 = (*raw_Y_ISOLATION_PIDK3);
      keep_Y_ISOLATION_PIDp3 = (*raw_Y_ISOLATION_PIDp3);
      keep_Y_ISOLATION_NNk3 = (*raw_Y_ISOLATION_NNk3);
      keep_Y_ISOLATION_NNpi3 = (*raw_Y_ISOLATION_NNpi3);
      keep_Y_ISOLATION_NNp3 = (*raw_Y_ISOLATION_NNp3);
      keep_Y_ISOLATION_IsMuon3 = (*raw_Y_ISOLATION_IsMuon3);
      keep_Y_ISOLATION_NNghost3 = (*raw_Y_ISOLATION_NNghost3);
      keep_Y_ISOLATION_TRUEID3 = (*raw_Y_ISOLATION_TRUEID3);
      keep_Y_ISOLATION_CHI24 = (*raw_Y_ISOLATION_CHI24);
      keep_Y_ISOLATION_SC4 = (*raw_Y_ISOLATION_SC4);
      keep_Y_ISOLATION_BDT4 = (*raw_Y_ISOLATION_BDT4);
      keep_Y_ISOLATION_ANGLE4 = (*raw_Y_ISOLATION_ANGLE4);
      keep_Y_ISOLATION_CHARGE4 = (*raw_Y_ISOLATION_CHARGE4);
      keep_Y_ISOLATION_Type4 = (*raw_Y_ISOLATION_Type4);
      keep_Y_ISOLATION_PE4 = (*raw_Y_ISOLATION_PE4);
      keep_Y_ISOLATION_PX4 = (*raw_Y_ISOLATION_PX4);
      keep_Y_ISOLATION_PY4 = (*raw_Y_ISOLATION_PY4);
      keep_Y_ISOLATION_PZ4 = (*raw_Y_ISOLATION_PZ4);
      keep_Y_ISOLATION_PIDK4 = (*raw_Y_ISOLATION_PIDK4);
      keep_Y_ISOLATION_PIDp4 = (*raw_Y_ISOLATION_PIDp4);
      keep_Y_ISOLATION_NNk4 = (*raw_Y_ISOLATION_NNk4);
      keep_Y_ISOLATION_NNpi4 = (*raw_Y_ISOLATION_NNpi4);
      keep_Y_ISOLATION_NNp4 = (*raw_Y_ISOLATION_NNp4);
      keep_Y_ISOLATION_IsMuon4 = (*raw_Y_ISOLATION_IsMuon4);
      keep_Y_ISOLATION_NNghost4 = (*raw_Y_ISOLATION_NNghost4);
      keep_Y_ISOLATION_TRUEID4 = (*raw_Y_ISOLATION_TRUEID4);
      keep_runNumber = (*raw_runNumber);
      keep_eventNumber = (*raw_eventNumber);
      keep_GpsTime = (*raw_GpsTime);
      rename_y_pt = (*raw_Y_PT);
      rename_y_px = (*raw_Y_PX);
      rename_y_py = (*raw_Y_PY);
      rename_y_pz = (*raw_Y_PZ);
      calculation_TempStuff = (*raw_D0_P)+(*raw_Y_PT);
      calculation_RandStuff = calculation_TempStuff*3.14;
      calculation_some_var = rename_y_pt + rename_y_pz;
      calculation_some_other_var = calculation_some_var*3.14;

      output.Fill();
    }
  }

  output_file->Write();
  delete output_file;
}


int main(int, char** argv) {
  TString in_prefix  = TString(argv[1]) + "/";
  TString out_prefix = TString(argv[2]) + "/";

  TFile *ntuple = new TFile(in_prefix + "../samples/sample.root");
  cout << "The ntuple being worked on is: " << "../samples/sample.root"
    << endl;

  vector<TFile*> friend_ntuples;
    friend_ntuples.push_back(new TFile(in_prefix + "../samples/sample_friend.root"));
    cout << "Additional friend ntuple: " << "../samples/sample_friend.root" << endl;

  // Define input trees and container to store associated friend trees
  auto tree_TupleB0_DecayTree = static_cast<TTree*>(ntuple->Get("TupleB0/DecayTree"));
  vector<TTree*> friends_TupleB0_DecayTree;
  auto tree_TupleB0WSPi_DecayTree = static_cast<TTree*>(ntuple->Get("TupleB0WSPi/DecayTree"));
  vector<TTree*> friends_TupleB0WSPi_DecayTree;

  // Handle friend trees
  TTree* tmp_tree;
  tmp_tree = static_cast<TTree*>(friend_ntuples[0]->Get("TupleB0/DecayTree"));
           tmp_tree->BuildIndex("runNumber", "eventNumber");
  tree_TupleB0_DecayTree->AddFriend(tmp_tree, "0", true);
           friends_TupleB0_DecayTree.push_back(tmp_tree);
           cout << "Handling input tree: " << "TupleB0/DecayTree" << endl;

  generator_ATuple(tree_TupleB0_DecayTree, out_prefix);
  generator_AnotherTuple(tree_TupleB0_DecayTree, out_prefix);
  generator_YetAnotherTuple(tree_TupleB0WSPi_DecayTree, out_prefix);

  // Cleanups
  cout <<"Cleanups" << endl;
  delete ntuple;
    for (auto tree : friends_TupleB0_DecayTree) delete tree;
    for (auto tree : friends_TupleB0WSPi_DecayTree) delete tree;
  for (auto ntp : friend_ntuples) delete ntp;

  return 0;
}

