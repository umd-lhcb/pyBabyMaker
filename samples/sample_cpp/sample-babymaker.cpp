// NOTE: This implementation is very naive.

#include <TFile.h>
#include <TTree.h>
#include <TTreeReader.h>
#include <TBranch.h>

// System headers
#include <cmath>
#include <iostream>

// User headers


// Generator for each output tree
void generator_ATuple(TFile *input_file, TFile *output_file) {
  TTreeReader reader("TupleB0/DecayTree", input_file);
  TTree output("ATuple", "ATuple");

  // Load needed branches from ntuple
  TTreeReaderValue<Double_t> raw_Y_PT(reader, "Y_PT");
  TTreeReaderValue<Double_t> raw_Y_PE(reader, "Y_PE");
  TTreeReaderValue<Double_t> raw_Y_PX(reader, "Y_PX");
  TTreeReaderValue<Double_t> raw_Y_PY(reader, "Y_PY");
  TTreeReaderValue<Double_t> raw_Y_PZ(reader, "Y_PZ");
  TTreeReaderValue<Double_t> raw_D0_P(reader, "D0_P");

  // Define output branches
  Double_t keep_Y_PE;
  output.Branch("Y_PE", &keep_Y_PE);
  Double_t rename_y_pt;
  output.Branch("y_pt", &rename_y_pt);
  Double_t rename_y_px;
  output.Branch("y_px", &rename_y_px);
  Double_t rename_y_py;
  output.Branch("y_py", &rename_y_py);
  Double_t rename_y_pz;
  output.Branch("y_pz", &rename_y_pz);
  Double_t calculation_RandStuff;
  output.Branch("RandStuff", &calculation_RandStuff);
  Double_t calculation_some_other_var;
  output.Branch("some_other_var", &calculation_some_other_var);
  Double_t calculation_alt_def;
  output.Branch("alt_def", &calculation_alt_def);

  // Define temporary variables
  Double_t calculation_TempStuff;
  Double_t calculation_some_var;

  while (reader.Next()) {
    // Define variables required by selection

    if ((true) && ((*raw_Y_PT) > 10000)) {
      // Assign values for each output branch in this loop
      keep_Y_PE = (*raw_Y_PE);
      rename_y_pt = (*raw_Y_PT);
      rename_y_px = (*raw_Y_PX);
      rename_y_py = (*raw_Y_PY);
      rename_y_pz = (*raw_Y_PZ);
      calculation_TempStuff = (*raw_D0_P)+(*raw_Y_PT);
      calculation_RandStuff = calculation_TempStuff;
      calculation_some_var = rename_y_pt + rename_y_pz;
      calculation_some_other_var = calculation_some_var;
      calculation_alt_def = (*raw_Y_PE);

      output.Fill();
    }
  }

  output_file->Write();
}

void generator_AnotherTuple(TFile *input_file, TFile *output_file) {
  TTreeReader reader("TupleB0/DecayTree", input_file);
  TTree output("AnotherTuple", "AnotherTuple");

  // Load needed branches from ntuple
  TTreeReaderValue<Double_t> raw_Y_PT(reader, "Y_PT");
  TTreeReaderValue<Double_t> raw_Y_PE(reader, "Y_PE");
  TTreeReaderValue<Double_t> raw_Y_PX(reader, "Y_PX");
  TTreeReaderValue<Double_t> raw_Y_PY(reader, "Y_PY");
  TTreeReaderValue<Double_t> raw_Y_PZ(reader, "Y_PZ");
  TTreeReaderValue<Double_t> raw_D0_P(reader, "D0_P");

  // Define output branches
  Double_t rename_b0_pt;
  output.Branch("b0_pt", &rename_b0_pt);
  Double_t keep_Y_PE;
  output.Branch("Y_PE", &keep_Y_PE);
  Double_t keep_Y_PX;
  output.Branch("Y_PX", &keep_Y_PX);
  Double_t keep_Y_PY;
  output.Branch("Y_PY", &keep_Y_PY);
  Double_t keep_Y_PZ;
  output.Branch("Y_PZ", &keep_Y_PZ);
  Double_t calculation_RandStuff;
  output.Branch("RandStuff", &calculation_RandStuff);

  // Define temporary variables
  Double_t calculation_TempStuff;

  while (reader.Next()) {
    // Define variables required by selection
    rename_b0_pt = (*raw_Y_PT);

    if ((true) && (rename_b0_pt > 10000) && ((*raw_Y_PE) > (100 * pow(10, 3)))) {
      // Assign values for each output branch in this loop
      keep_Y_PE = (*raw_Y_PE);
      keep_Y_PX = (*raw_Y_PX);
      keep_Y_PY = (*raw_Y_PY);
      keep_Y_PZ = (*raw_Y_PZ);
      calculation_TempStuff = (*raw_D0_P)+(*raw_Y_PT);
      calculation_RandStuff = calculation_TempStuff;

      output.Fill();
    }
  }

  output_file->Write();
}

void generator_YetAnotherTuple(TFile *input_file, TFile *output_file) {
  TTreeReader reader("TupleB0WSPi/DecayTree", input_file);
  TTree output("YetAnotherTuple", "YetAnotherTuple");

  // Load needed branches from ntuple
  TTreeReaderValue<Bool_t> raw_piminus_isMuon(reader, "piminus_isMuon");
  TTreeReaderValue<Double_t> raw_Y_OWNPV_X(reader, "Y_OWNPV_X");
  TTreeReaderValue<Double_t> raw_Y_OWNPV_Y(reader, "Y_OWNPV_Y");
  TTreeReaderValue<Double_t> raw_Y_OWNPV_Z(reader, "Y_OWNPV_Z");
  TTreeReaderValue<Double_t> raw_Y_OWNPV_XERR(reader, "Y_OWNPV_XERR");
  TTreeReaderValue<Double_t> raw_Y_OWNPV_YERR(reader, "Y_OWNPV_YERR");
  TTreeReaderValue<Double_t> raw_Y_OWNPV_ZERR(reader, "Y_OWNPV_ZERR");
  TTreeReaderValue<Double_t> raw_Y_OWNPV_CHI2(reader, "Y_OWNPV_CHI2");
  TTreeReaderValue<Int_t> raw_Y_OWNPV_NDOF(reader, "Y_OWNPV_NDOF");
  TTreeReaderValue<Double_t> raw_Y_PE(reader, "Y_PE");
  TTreeReaderValue<Double_t> raw_Y_ISOLATION_CHI2(reader, "Y_ISOLATION_CHI2");
  TTreeReaderValue<Double_t> raw_Y_ISOLATION_ANGLE(reader, "Y_ISOLATION_ANGLE");
  TTreeReaderValue<Int_t> raw_Y_ISOLATION_SC(reader, "Y_ISOLATION_SC");
  TTreeReaderValue<Double_t> raw_Y_ISOLATION_BDT(reader, "Y_ISOLATION_BDT");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_CHARGE(reader, "Y_ISOLATION_CHARGE");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_Type(reader, "Y_ISOLATION_Type");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_PE(reader, "Y_ISOLATION_PE");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_PX(reader, "Y_ISOLATION_PX");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_PY(reader, "Y_ISOLATION_PY");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_PZ(reader, "Y_ISOLATION_PZ");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_PIDK(reader, "Y_ISOLATION_PIDK");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_PIDp(reader, "Y_ISOLATION_PIDp");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_NNk(reader, "Y_ISOLATION_NNk");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_NNpi(reader, "Y_ISOLATION_NNpi");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_NNp(reader, "Y_ISOLATION_NNp");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_IsMuon(reader, "Y_ISOLATION_IsMuon");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_NNghost(reader, "Y_ISOLATION_NNghost");
  TTreeReaderValue<Int_t> raw_Y_ISOLATION_TRUEID(reader, "Y_ISOLATION_TRUEID");
  TTreeReaderValue<Double_t> raw_Y_ISOLATION_CHI22(reader, "Y_ISOLATION_CHI22");
  TTreeReaderValue<Int_t> raw_Y_ISOLATION_SC2(reader, "Y_ISOLATION_SC2");
  TTreeReaderValue<Double_t> raw_Y_ISOLATION_ANGLE2(reader, "Y_ISOLATION_ANGLE2");
  TTreeReaderValue<Double_t> raw_Y_ISOLATION_BDT2(reader, "Y_ISOLATION_BDT2");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_CHARGE2(reader, "Y_ISOLATION_CHARGE2");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_Type2(reader, "Y_ISOLATION_Type2");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_PE2(reader, "Y_ISOLATION_PE2");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_PX2(reader, "Y_ISOLATION_PX2");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_PY2(reader, "Y_ISOLATION_PY2");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_PZ2(reader, "Y_ISOLATION_PZ2");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_PIDK2(reader, "Y_ISOLATION_PIDK2");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_PIDp2(reader, "Y_ISOLATION_PIDp2");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_NNk2(reader, "Y_ISOLATION_NNk2");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_NNpi2(reader, "Y_ISOLATION_NNpi2");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_NNp2(reader, "Y_ISOLATION_NNp2");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_IsMuon2(reader, "Y_ISOLATION_IsMuon2");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_NNghost2(reader, "Y_ISOLATION_NNghost2");
  TTreeReaderValue<Int_t> raw_Y_ISOLATION_TRUEID2(reader, "Y_ISOLATION_TRUEID2");
  TTreeReaderValue<Double_t> raw_Y_ISOLATION_CHI23(reader, "Y_ISOLATION_CHI23");
  TTreeReaderValue<Int_t> raw_Y_ISOLATION_SC3(reader, "Y_ISOLATION_SC3");
  TTreeReaderValue<Double_t> raw_Y_ISOLATION_BDT3(reader, "Y_ISOLATION_BDT3");
  TTreeReaderValue<Double_t> raw_Y_ISOLATION_ANGLE3(reader, "Y_ISOLATION_ANGLE3");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_CHARGE3(reader, "Y_ISOLATION_CHARGE3");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_Type3(reader, "Y_ISOLATION_Type3");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_PE3(reader, "Y_ISOLATION_PE3");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_PX3(reader, "Y_ISOLATION_PX3");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_PY3(reader, "Y_ISOLATION_PY3");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_PZ3(reader, "Y_ISOLATION_PZ3");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_PIDK3(reader, "Y_ISOLATION_PIDK3");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_PIDp3(reader, "Y_ISOLATION_PIDp3");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_NNk3(reader, "Y_ISOLATION_NNk3");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_NNpi3(reader, "Y_ISOLATION_NNpi3");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_NNp3(reader, "Y_ISOLATION_NNp3");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_IsMuon3(reader, "Y_ISOLATION_IsMuon3");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_NNghost3(reader, "Y_ISOLATION_NNghost3");
  TTreeReaderValue<Int_t> raw_Y_ISOLATION_TRUEID3(reader, "Y_ISOLATION_TRUEID3");
  TTreeReaderValue<Double_t> raw_Y_ISOLATION_CHI24(reader, "Y_ISOLATION_CHI24");
  TTreeReaderValue<Int_t> raw_Y_ISOLATION_SC4(reader, "Y_ISOLATION_SC4");
  TTreeReaderValue<Double_t> raw_Y_ISOLATION_BDT4(reader, "Y_ISOLATION_BDT4");
  TTreeReaderValue<Double_t> raw_Y_ISOLATION_ANGLE4(reader, "Y_ISOLATION_ANGLE4");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_CHARGE4(reader, "Y_ISOLATION_CHARGE4");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_Type4(reader, "Y_ISOLATION_Type4");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_PE4(reader, "Y_ISOLATION_PE4");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_PX4(reader, "Y_ISOLATION_PX4");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_PY4(reader, "Y_ISOLATION_PY4");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_PZ4(reader, "Y_ISOLATION_PZ4");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_PIDK4(reader, "Y_ISOLATION_PIDK4");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_PIDp4(reader, "Y_ISOLATION_PIDp4");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_NNk4(reader, "Y_ISOLATION_NNk4");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_NNpi4(reader, "Y_ISOLATION_NNpi4");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_NNp4(reader, "Y_ISOLATION_NNp4");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_IsMuon4(reader, "Y_ISOLATION_IsMuon4");
  TTreeReaderValue<Float_t> raw_Y_ISOLATION_NNghost4(reader, "Y_ISOLATION_NNghost4");
  TTreeReaderValue<Int_t> raw_Y_ISOLATION_TRUEID4(reader, "Y_ISOLATION_TRUEID4");
  TTreeReaderValue<Double_t> raw_Y_PT(reader, "Y_PT");
  TTreeReaderValue<Double_t> raw_Y_PX(reader, "Y_PX");
  TTreeReaderValue<Double_t> raw_Y_PY(reader, "Y_PY");
  TTreeReaderValue<Double_t> raw_Y_PZ(reader, "Y_PZ");
  TTreeReaderValue<Double_t> raw_D0_P(reader, "D0_P");

  // Define output branches
  Double_t keep_Y_OWNPV_X;
  output.Branch("Y_OWNPV_X", &keep_Y_OWNPV_X);
  Double_t keep_Y_OWNPV_Y;
  output.Branch("Y_OWNPV_Y", &keep_Y_OWNPV_Y);
  Double_t keep_Y_OWNPV_Z;
  output.Branch("Y_OWNPV_Z", &keep_Y_OWNPV_Z);
  Double_t keep_Y_OWNPV_XERR;
  output.Branch("Y_OWNPV_XERR", &keep_Y_OWNPV_XERR);
  Double_t keep_Y_OWNPV_YERR;
  output.Branch("Y_OWNPV_YERR", &keep_Y_OWNPV_YERR);
  Double_t keep_Y_OWNPV_ZERR;
  output.Branch("Y_OWNPV_ZERR", &keep_Y_OWNPV_ZERR);
  Double_t keep_Y_OWNPV_CHI2;
  output.Branch("Y_OWNPV_CHI2", &keep_Y_OWNPV_CHI2);
  Int_t keep_Y_OWNPV_NDOF;
  output.Branch("Y_OWNPV_NDOF", &keep_Y_OWNPV_NDOF);
  Double_t keep_Y_PE;
  output.Branch("Y_PE", &keep_Y_PE);
  Double_t keep_Y_ISOLATION_CHI2;
  output.Branch("Y_ISOLATION_CHI2", &keep_Y_ISOLATION_CHI2);
  Double_t keep_Y_ISOLATION_ANGLE;
  output.Branch("Y_ISOLATION_ANGLE", &keep_Y_ISOLATION_ANGLE);
  Int_t keep_Y_ISOLATION_SC;
  output.Branch("Y_ISOLATION_SC", &keep_Y_ISOLATION_SC);
  Double_t keep_Y_ISOLATION_BDT;
  output.Branch("Y_ISOLATION_BDT", &keep_Y_ISOLATION_BDT);
  Float_t keep_Y_ISOLATION_CHARGE;
  output.Branch("Y_ISOLATION_CHARGE", &keep_Y_ISOLATION_CHARGE);
  Float_t keep_Y_ISOLATION_Type;
  output.Branch("Y_ISOLATION_Type", &keep_Y_ISOLATION_Type);
  Float_t keep_Y_ISOLATION_PE;
  output.Branch("Y_ISOLATION_PE", &keep_Y_ISOLATION_PE);
  Float_t keep_Y_ISOLATION_PX;
  output.Branch("Y_ISOLATION_PX", &keep_Y_ISOLATION_PX);
  Float_t keep_Y_ISOLATION_PY;
  output.Branch("Y_ISOLATION_PY", &keep_Y_ISOLATION_PY);
  Float_t keep_Y_ISOLATION_PZ;
  output.Branch("Y_ISOLATION_PZ", &keep_Y_ISOLATION_PZ);
  Float_t keep_Y_ISOLATION_PIDK;
  output.Branch("Y_ISOLATION_PIDK", &keep_Y_ISOLATION_PIDK);
  Float_t keep_Y_ISOLATION_PIDp;
  output.Branch("Y_ISOLATION_PIDp", &keep_Y_ISOLATION_PIDp);
  Float_t keep_Y_ISOLATION_NNk;
  output.Branch("Y_ISOLATION_NNk", &keep_Y_ISOLATION_NNk);
  Float_t keep_Y_ISOLATION_NNpi;
  output.Branch("Y_ISOLATION_NNpi", &keep_Y_ISOLATION_NNpi);
  Float_t keep_Y_ISOLATION_NNp;
  output.Branch("Y_ISOLATION_NNp", &keep_Y_ISOLATION_NNp);
  Float_t keep_Y_ISOLATION_IsMuon;
  output.Branch("Y_ISOLATION_IsMuon", &keep_Y_ISOLATION_IsMuon);
  Float_t keep_Y_ISOLATION_NNghost;
  output.Branch("Y_ISOLATION_NNghost", &keep_Y_ISOLATION_NNghost);
  Int_t keep_Y_ISOLATION_TRUEID;
  output.Branch("Y_ISOLATION_TRUEID", &keep_Y_ISOLATION_TRUEID);
  Double_t keep_Y_ISOLATION_CHI22;
  output.Branch("Y_ISOLATION_CHI22", &keep_Y_ISOLATION_CHI22);
  Int_t keep_Y_ISOLATION_SC2;
  output.Branch("Y_ISOLATION_SC2", &keep_Y_ISOLATION_SC2);
  Double_t keep_Y_ISOLATION_ANGLE2;
  output.Branch("Y_ISOLATION_ANGLE2", &keep_Y_ISOLATION_ANGLE2);
  Double_t keep_Y_ISOLATION_BDT2;
  output.Branch("Y_ISOLATION_BDT2", &keep_Y_ISOLATION_BDT2);
  Float_t keep_Y_ISOLATION_CHARGE2;
  output.Branch("Y_ISOLATION_CHARGE2", &keep_Y_ISOLATION_CHARGE2);
  Float_t keep_Y_ISOLATION_Type2;
  output.Branch("Y_ISOLATION_Type2", &keep_Y_ISOLATION_Type2);
  Float_t keep_Y_ISOLATION_PE2;
  output.Branch("Y_ISOLATION_PE2", &keep_Y_ISOLATION_PE2);
  Float_t keep_Y_ISOLATION_PX2;
  output.Branch("Y_ISOLATION_PX2", &keep_Y_ISOLATION_PX2);
  Float_t keep_Y_ISOLATION_PY2;
  output.Branch("Y_ISOLATION_PY2", &keep_Y_ISOLATION_PY2);
  Float_t keep_Y_ISOLATION_PZ2;
  output.Branch("Y_ISOLATION_PZ2", &keep_Y_ISOLATION_PZ2);
  Float_t keep_Y_ISOLATION_PIDK2;
  output.Branch("Y_ISOLATION_PIDK2", &keep_Y_ISOLATION_PIDK2);
  Float_t keep_Y_ISOLATION_PIDp2;
  output.Branch("Y_ISOLATION_PIDp2", &keep_Y_ISOLATION_PIDp2);
  Float_t keep_Y_ISOLATION_NNk2;
  output.Branch("Y_ISOLATION_NNk2", &keep_Y_ISOLATION_NNk2);
  Float_t keep_Y_ISOLATION_NNpi2;
  output.Branch("Y_ISOLATION_NNpi2", &keep_Y_ISOLATION_NNpi2);
  Float_t keep_Y_ISOLATION_NNp2;
  output.Branch("Y_ISOLATION_NNp2", &keep_Y_ISOLATION_NNp2);
  Float_t keep_Y_ISOLATION_IsMuon2;
  output.Branch("Y_ISOLATION_IsMuon2", &keep_Y_ISOLATION_IsMuon2);
  Float_t keep_Y_ISOLATION_NNghost2;
  output.Branch("Y_ISOLATION_NNghost2", &keep_Y_ISOLATION_NNghost2);
  Int_t keep_Y_ISOLATION_TRUEID2;
  output.Branch("Y_ISOLATION_TRUEID2", &keep_Y_ISOLATION_TRUEID2);
  Double_t keep_Y_ISOLATION_CHI23;
  output.Branch("Y_ISOLATION_CHI23", &keep_Y_ISOLATION_CHI23);
  Int_t keep_Y_ISOLATION_SC3;
  output.Branch("Y_ISOLATION_SC3", &keep_Y_ISOLATION_SC3);
  Double_t keep_Y_ISOLATION_BDT3;
  output.Branch("Y_ISOLATION_BDT3", &keep_Y_ISOLATION_BDT3);
  Double_t keep_Y_ISOLATION_ANGLE3;
  output.Branch("Y_ISOLATION_ANGLE3", &keep_Y_ISOLATION_ANGLE3);
  Float_t keep_Y_ISOLATION_CHARGE3;
  output.Branch("Y_ISOLATION_CHARGE3", &keep_Y_ISOLATION_CHARGE3);
  Float_t keep_Y_ISOLATION_Type3;
  output.Branch("Y_ISOLATION_Type3", &keep_Y_ISOLATION_Type3);
  Float_t keep_Y_ISOLATION_PE3;
  output.Branch("Y_ISOLATION_PE3", &keep_Y_ISOLATION_PE3);
  Float_t keep_Y_ISOLATION_PX3;
  output.Branch("Y_ISOLATION_PX3", &keep_Y_ISOLATION_PX3);
  Float_t keep_Y_ISOLATION_PY3;
  output.Branch("Y_ISOLATION_PY3", &keep_Y_ISOLATION_PY3);
  Float_t keep_Y_ISOLATION_PZ3;
  output.Branch("Y_ISOLATION_PZ3", &keep_Y_ISOLATION_PZ3);
  Float_t keep_Y_ISOLATION_PIDK3;
  output.Branch("Y_ISOLATION_PIDK3", &keep_Y_ISOLATION_PIDK3);
  Float_t keep_Y_ISOLATION_PIDp3;
  output.Branch("Y_ISOLATION_PIDp3", &keep_Y_ISOLATION_PIDp3);
  Float_t keep_Y_ISOLATION_NNk3;
  output.Branch("Y_ISOLATION_NNk3", &keep_Y_ISOLATION_NNk3);
  Float_t keep_Y_ISOLATION_NNpi3;
  output.Branch("Y_ISOLATION_NNpi3", &keep_Y_ISOLATION_NNpi3);
  Float_t keep_Y_ISOLATION_NNp3;
  output.Branch("Y_ISOLATION_NNp3", &keep_Y_ISOLATION_NNp3);
  Float_t keep_Y_ISOLATION_IsMuon3;
  output.Branch("Y_ISOLATION_IsMuon3", &keep_Y_ISOLATION_IsMuon3);
  Float_t keep_Y_ISOLATION_NNghost3;
  output.Branch("Y_ISOLATION_NNghost3", &keep_Y_ISOLATION_NNghost3);
  Int_t keep_Y_ISOLATION_TRUEID3;
  output.Branch("Y_ISOLATION_TRUEID3", &keep_Y_ISOLATION_TRUEID3);
  Double_t keep_Y_ISOLATION_CHI24;
  output.Branch("Y_ISOLATION_CHI24", &keep_Y_ISOLATION_CHI24);
  Int_t keep_Y_ISOLATION_SC4;
  output.Branch("Y_ISOLATION_SC4", &keep_Y_ISOLATION_SC4);
  Double_t keep_Y_ISOLATION_BDT4;
  output.Branch("Y_ISOLATION_BDT4", &keep_Y_ISOLATION_BDT4);
  Double_t keep_Y_ISOLATION_ANGLE4;
  output.Branch("Y_ISOLATION_ANGLE4", &keep_Y_ISOLATION_ANGLE4);
  Float_t keep_Y_ISOLATION_CHARGE4;
  output.Branch("Y_ISOLATION_CHARGE4", &keep_Y_ISOLATION_CHARGE4);
  Float_t keep_Y_ISOLATION_Type4;
  output.Branch("Y_ISOLATION_Type4", &keep_Y_ISOLATION_Type4);
  Float_t keep_Y_ISOLATION_PE4;
  output.Branch("Y_ISOLATION_PE4", &keep_Y_ISOLATION_PE4);
  Float_t keep_Y_ISOLATION_PX4;
  output.Branch("Y_ISOLATION_PX4", &keep_Y_ISOLATION_PX4);
  Float_t keep_Y_ISOLATION_PY4;
  output.Branch("Y_ISOLATION_PY4", &keep_Y_ISOLATION_PY4);
  Float_t keep_Y_ISOLATION_PZ4;
  output.Branch("Y_ISOLATION_PZ4", &keep_Y_ISOLATION_PZ4);
  Float_t keep_Y_ISOLATION_PIDK4;
  output.Branch("Y_ISOLATION_PIDK4", &keep_Y_ISOLATION_PIDK4);
  Float_t keep_Y_ISOLATION_PIDp4;
  output.Branch("Y_ISOLATION_PIDp4", &keep_Y_ISOLATION_PIDp4);
  Float_t keep_Y_ISOLATION_NNk4;
  output.Branch("Y_ISOLATION_NNk4", &keep_Y_ISOLATION_NNk4);
  Float_t keep_Y_ISOLATION_NNpi4;
  output.Branch("Y_ISOLATION_NNpi4", &keep_Y_ISOLATION_NNpi4);
  Float_t keep_Y_ISOLATION_NNp4;
  output.Branch("Y_ISOLATION_NNp4", &keep_Y_ISOLATION_NNp4);
  Float_t keep_Y_ISOLATION_IsMuon4;
  output.Branch("Y_ISOLATION_IsMuon4", &keep_Y_ISOLATION_IsMuon4);
  Float_t keep_Y_ISOLATION_NNghost4;
  output.Branch("Y_ISOLATION_NNghost4", &keep_Y_ISOLATION_NNghost4);
  Int_t keep_Y_ISOLATION_TRUEID4;
  output.Branch("Y_ISOLATION_TRUEID4", &keep_Y_ISOLATION_TRUEID4);
  Double_t rename_y_pt;
  output.Branch("y_pt", &rename_y_pt);
  Double_t rename_y_px;
  output.Branch("y_px", &rename_y_px);
  Double_t rename_y_py;
  output.Branch("y_py", &rename_y_py);
  Double_t rename_y_pz;
  output.Branch("y_pz", &rename_y_pz);
  Double_t calculation_RandStuff;
  output.Branch("RandStuff", &calculation_RandStuff);
  Double_t calculation_some_other_var;
  output.Branch("some_other_var", &calculation_some_other_var);

  // Define temporary variables
  Double_t calculation_TempStuff;
  Double_t calculation_some_var;

  while (reader.Next()) {
    // Define variables required by selection

    if ((true) && ((*raw_piminus_isMuon))) {
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
      rename_y_pt = (*raw_Y_PT);
      rename_y_px = (*raw_Y_PX);
      rename_y_py = (*raw_Y_PY);
      rename_y_pz = (*raw_Y_PZ);
      calculation_TempStuff = (*raw_D0_P)+(*raw_Y_PT);
      calculation_RandStuff = calculation_TempStuff;
      calculation_some_var = rename_y_pt + rename_y_pz;
      calculation_some_other_var = calculation_some_var;

      output.Fill();
    }
  }

  output_file->Write();
}


int main(int, char** argv) {
  TFile *input_file = new TFile(argv[1], "read");
  TFile *output_file = new TFile(argv[2], "recreate");

  generator_ATuple(input_file, output_file);
  generator_AnotherTuple(input_file, output_file);
  generator_YetAnotherTuple(input_file, output_file);

  output_file->Close();

  delete input_file;
  delete output_file;

  return 0;
}

