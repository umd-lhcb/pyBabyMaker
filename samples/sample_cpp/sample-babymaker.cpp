#include <TFile.h>
#include <TTree.h>
#include <TTreeReader.h>
#include <TBranch.h>
#include <cmath>
#include <iostream>


void generator_ATuple(TFile *input_file, TFile *output_file) {
  TTreeReader reader("TupleB0/DecayTree", input_file);

  TTree output("ATuple", "ATuple");


  TTreeReaderValue<Double_t> Y_PT(reader, "Y_PT");
TTreeReaderValue<Double_t> Y_PE(reader, "Y_PE");
TTreeReaderValue<Double_t> Y_PX(reader, "Y_PX");
TTreeReaderValue<Double_t> Y_PY(reader, "Y_PY");
TTreeReaderValue<Double_t> Y_PZ(reader, "Y_PZ");
TTreeReaderValue<Double_t> D0_P(reader, "D0_P");

  Double_t y_pt_out;
output.Branch("y_pt", &y_pt_out);
Double_t Y_PE_out;
output.Branch("Y_PE", &Y_PE_out);
Double_t y_px_out;
output.Branch("y_px", &y_px_out);
Double_t y_py_out;
output.Branch("y_py", &y_py_out);
Double_t y_pz_out;
output.Branch("y_pz", &y_pz_out);
Double_t RandStuff_out;
output.Branch("RandStuff", &RandStuff_out);


  while (reader.Next()) {
    Double_t TempStuff = (*D0_P)+(*Y_PT);

    if ((*Y_PT) > 10000) {
  y_pt_out = (*Y_PT);
Y_PE_out = (*Y_PE);
y_px_out = (*Y_PX);
y_py_out = (*Y_PY);
y_pz_out = (*Y_PZ);
RandStuff_out = TempStuff;

  output.Fill();
}
  }

  output_file->Write();
}

void generator_AnotherTuple(TFile *input_file, TFile *output_file) {
  TTreeReader reader("TupleB0/DecayTree", input_file);

  TTree output("AnotherTuple", "AnotherTuple");


  TTreeReaderValue<Double_t> Y_PT(reader, "Y_PT");
TTreeReaderValue<Double_t> Y_PE(reader, "Y_PE");

  Double_t Y_PT_out;
output.Branch("Y_PT", &Y_PT_out);


  while (reader.Next()) {
    
    if ((*Y_PT) > 10000 && (*Y_PE) > (100 * pow(10, 3))) {
  Y_PT_out = (*Y_PT);

  output.Fill();
}
  }

  output_file->Write();
}

void generator_YetAnotherTuple(TFile *input_file, TFile *output_file) {
  TTreeReader reader("TupleB0WSPi/DecayTree", input_file);

  TTree output("YetAnotherTuple", "YetAnotherTuple");


  TTreeReaderValue<Double_t> Y_OWNPV_X(reader, "Y_OWNPV_X");
TTreeReaderValue<Double_t> Y_OWNPV_Y(reader, "Y_OWNPV_Y");
TTreeReaderValue<Double_t> Y_OWNPV_Z(reader, "Y_OWNPV_Z");
TTreeReaderValue<Double_t> Y_OWNPV_XERR(reader, "Y_OWNPV_XERR");
TTreeReaderValue<Double_t> Y_OWNPV_YERR(reader, "Y_OWNPV_YERR");
TTreeReaderValue<Double_t> Y_OWNPV_ZERR(reader, "Y_OWNPV_ZERR");
TTreeReaderValue<Double_t> Y_OWNPV_CHI2(reader, "Y_OWNPV_CHI2");
TTreeReaderValue<Int_t> Y_OWNPV_NDOF(reader, "Y_OWNPV_NDOF");
TTreeReaderValue<Double_t> Y_ISOLATION_CHI2(reader, "Y_ISOLATION_CHI2");
TTreeReaderValue<Double_t> Y_ISOLATION_ANGLE(reader, "Y_ISOLATION_ANGLE");
TTreeReaderValue<Int_t> Y_ISOLATION_SC(reader, "Y_ISOLATION_SC");
TTreeReaderValue<Double_t> Y_ISOLATION_BDT(reader, "Y_ISOLATION_BDT");
TTreeReaderValue<Float_t> Y_ISOLATION_CHARGE(reader, "Y_ISOLATION_CHARGE");
TTreeReaderValue<Float_t> Y_ISOLATION_Type(reader, "Y_ISOLATION_Type");
TTreeReaderValue<Float_t> Y_ISOLATION_PE(reader, "Y_ISOLATION_PE");
TTreeReaderValue<Float_t> Y_ISOLATION_PX(reader, "Y_ISOLATION_PX");
TTreeReaderValue<Float_t> Y_ISOLATION_PY(reader, "Y_ISOLATION_PY");
TTreeReaderValue<Float_t> Y_ISOLATION_PZ(reader, "Y_ISOLATION_PZ");
TTreeReaderValue<Float_t> Y_ISOLATION_PIDK(reader, "Y_ISOLATION_PIDK");
TTreeReaderValue<Float_t> Y_ISOLATION_PIDp(reader, "Y_ISOLATION_PIDp");
TTreeReaderValue<Float_t> Y_ISOLATION_NNk(reader, "Y_ISOLATION_NNk");
TTreeReaderValue<Float_t> Y_ISOLATION_NNpi(reader, "Y_ISOLATION_NNpi");
TTreeReaderValue<Float_t> Y_ISOLATION_NNp(reader, "Y_ISOLATION_NNp");
TTreeReaderValue<Float_t> Y_ISOLATION_IsMuon(reader, "Y_ISOLATION_IsMuon");
TTreeReaderValue<Float_t> Y_ISOLATION_NNghost(reader, "Y_ISOLATION_NNghost");
TTreeReaderValue<Int_t> Y_ISOLATION_TRUEID(reader, "Y_ISOLATION_TRUEID");
TTreeReaderValue<Double_t> Y_ISOLATION_CHI22(reader, "Y_ISOLATION_CHI22");
TTreeReaderValue<Int_t> Y_ISOLATION_SC2(reader, "Y_ISOLATION_SC2");
TTreeReaderValue<Double_t> Y_ISOLATION_ANGLE2(reader, "Y_ISOLATION_ANGLE2");
TTreeReaderValue<Double_t> Y_ISOLATION_BDT2(reader, "Y_ISOLATION_BDT2");
TTreeReaderValue<Float_t> Y_ISOLATION_CHARGE2(reader, "Y_ISOLATION_CHARGE2");
TTreeReaderValue<Float_t> Y_ISOLATION_Type2(reader, "Y_ISOLATION_Type2");
TTreeReaderValue<Float_t> Y_ISOLATION_PE2(reader, "Y_ISOLATION_PE2");
TTreeReaderValue<Float_t> Y_ISOLATION_PX2(reader, "Y_ISOLATION_PX2");
TTreeReaderValue<Float_t> Y_ISOLATION_PY2(reader, "Y_ISOLATION_PY2");
TTreeReaderValue<Float_t> Y_ISOLATION_PZ2(reader, "Y_ISOLATION_PZ2");
TTreeReaderValue<Float_t> Y_ISOLATION_PIDK2(reader, "Y_ISOLATION_PIDK2");
TTreeReaderValue<Float_t> Y_ISOLATION_PIDp2(reader, "Y_ISOLATION_PIDp2");
TTreeReaderValue<Float_t> Y_ISOLATION_NNk2(reader, "Y_ISOLATION_NNk2");
TTreeReaderValue<Float_t> Y_ISOLATION_NNpi2(reader, "Y_ISOLATION_NNpi2");
TTreeReaderValue<Float_t> Y_ISOLATION_NNp2(reader, "Y_ISOLATION_NNp2");
TTreeReaderValue<Float_t> Y_ISOLATION_IsMuon2(reader, "Y_ISOLATION_IsMuon2");
TTreeReaderValue<Float_t> Y_ISOLATION_NNghost2(reader, "Y_ISOLATION_NNghost2");
TTreeReaderValue<Int_t> Y_ISOLATION_TRUEID2(reader, "Y_ISOLATION_TRUEID2");
TTreeReaderValue<Double_t> Y_ISOLATION_CHI23(reader, "Y_ISOLATION_CHI23");
TTreeReaderValue<Int_t> Y_ISOLATION_SC3(reader, "Y_ISOLATION_SC3");
TTreeReaderValue<Double_t> Y_ISOLATION_BDT3(reader, "Y_ISOLATION_BDT3");
TTreeReaderValue<Double_t> Y_ISOLATION_ANGLE3(reader, "Y_ISOLATION_ANGLE3");
TTreeReaderValue<Float_t> Y_ISOLATION_CHARGE3(reader, "Y_ISOLATION_CHARGE3");
TTreeReaderValue<Float_t> Y_ISOLATION_Type3(reader, "Y_ISOLATION_Type3");
TTreeReaderValue<Float_t> Y_ISOLATION_PE3(reader, "Y_ISOLATION_PE3");
TTreeReaderValue<Float_t> Y_ISOLATION_PX3(reader, "Y_ISOLATION_PX3");
TTreeReaderValue<Float_t> Y_ISOLATION_PY3(reader, "Y_ISOLATION_PY3");
TTreeReaderValue<Float_t> Y_ISOLATION_PZ3(reader, "Y_ISOLATION_PZ3");
TTreeReaderValue<Float_t> Y_ISOLATION_PIDK3(reader, "Y_ISOLATION_PIDK3");
TTreeReaderValue<Float_t> Y_ISOLATION_PIDp3(reader, "Y_ISOLATION_PIDp3");
TTreeReaderValue<Float_t> Y_ISOLATION_NNk3(reader, "Y_ISOLATION_NNk3");
TTreeReaderValue<Float_t> Y_ISOLATION_NNpi3(reader, "Y_ISOLATION_NNpi3");
TTreeReaderValue<Float_t> Y_ISOLATION_NNp3(reader, "Y_ISOLATION_NNp3");
TTreeReaderValue<Float_t> Y_ISOLATION_IsMuon3(reader, "Y_ISOLATION_IsMuon3");
TTreeReaderValue<Float_t> Y_ISOLATION_NNghost3(reader, "Y_ISOLATION_NNghost3");
TTreeReaderValue<Int_t> Y_ISOLATION_TRUEID3(reader, "Y_ISOLATION_TRUEID3");
TTreeReaderValue<Double_t> Y_ISOLATION_CHI24(reader, "Y_ISOLATION_CHI24");
TTreeReaderValue<Int_t> Y_ISOLATION_SC4(reader, "Y_ISOLATION_SC4");
TTreeReaderValue<Double_t> Y_ISOLATION_BDT4(reader, "Y_ISOLATION_BDT4");
TTreeReaderValue<Double_t> Y_ISOLATION_ANGLE4(reader, "Y_ISOLATION_ANGLE4");
TTreeReaderValue<Float_t> Y_ISOLATION_CHARGE4(reader, "Y_ISOLATION_CHARGE4");
TTreeReaderValue<Float_t> Y_ISOLATION_Type4(reader, "Y_ISOLATION_Type4");
TTreeReaderValue<Float_t> Y_ISOLATION_PE4(reader, "Y_ISOLATION_PE4");
TTreeReaderValue<Float_t> Y_ISOLATION_PX4(reader, "Y_ISOLATION_PX4");
TTreeReaderValue<Float_t> Y_ISOLATION_PY4(reader, "Y_ISOLATION_PY4");
TTreeReaderValue<Float_t> Y_ISOLATION_PZ4(reader, "Y_ISOLATION_PZ4");
TTreeReaderValue<Float_t> Y_ISOLATION_PIDK4(reader, "Y_ISOLATION_PIDK4");
TTreeReaderValue<Float_t> Y_ISOLATION_PIDp4(reader, "Y_ISOLATION_PIDp4");
TTreeReaderValue<Float_t> Y_ISOLATION_NNk4(reader, "Y_ISOLATION_NNk4");
TTreeReaderValue<Float_t> Y_ISOLATION_NNpi4(reader, "Y_ISOLATION_NNpi4");
TTreeReaderValue<Float_t> Y_ISOLATION_NNp4(reader, "Y_ISOLATION_NNp4");
TTreeReaderValue<Float_t> Y_ISOLATION_IsMuon4(reader, "Y_ISOLATION_IsMuon4");
TTreeReaderValue<Float_t> Y_ISOLATION_NNghost4(reader, "Y_ISOLATION_NNghost4");
TTreeReaderValue<Int_t> Y_ISOLATION_TRUEID4(reader, "Y_ISOLATION_TRUEID4");

  Double_t Y_OWNPV_X_out;
output.Branch("Y_OWNPV_X", &Y_OWNPV_X_out);
Double_t Y_OWNPV_Y_out;
output.Branch("Y_OWNPV_Y", &Y_OWNPV_Y_out);
Double_t Y_OWNPV_Z_out;
output.Branch("Y_OWNPV_Z", &Y_OWNPV_Z_out);
Double_t Y_OWNPV_XERR_out;
output.Branch("Y_OWNPV_XERR", &Y_OWNPV_XERR_out);
Double_t Y_OWNPV_YERR_out;
output.Branch("Y_OWNPV_YERR", &Y_OWNPV_YERR_out);
Double_t Y_OWNPV_ZERR_out;
output.Branch("Y_OWNPV_ZERR", &Y_OWNPV_ZERR_out);
Double_t Y_OWNPV_CHI2_out;
output.Branch("Y_OWNPV_CHI2", &Y_OWNPV_CHI2_out);
Int_t Y_OWNPV_NDOF_out;
output.Branch("Y_OWNPV_NDOF", &Y_OWNPV_NDOF_out);
Double_t Y_ISOLATION_CHI2_out;
output.Branch("Y_ISOLATION_CHI2", &Y_ISOLATION_CHI2_out);
Double_t Y_ISOLATION_ANGLE_out;
output.Branch("Y_ISOLATION_ANGLE", &Y_ISOLATION_ANGLE_out);
Int_t Y_ISOLATION_SC_out;
output.Branch("Y_ISOLATION_SC", &Y_ISOLATION_SC_out);
Double_t Y_ISOLATION_BDT_out;
output.Branch("Y_ISOLATION_BDT", &Y_ISOLATION_BDT_out);
Float_t Y_ISOLATION_CHARGE_out;
output.Branch("Y_ISOLATION_CHARGE", &Y_ISOLATION_CHARGE_out);
Float_t Y_ISOLATION_Type_out;
output.Branch("Y_ISOLATION_Type", &Y_ISOLATION_Type_out);
Float_t Y_ISOLATION_PE_out;
output.Branch("Y_ISOLATION_PE", &Y_ISOLATION_PE_out);
Float_t Y_ISOLATION_PX_out;
output.Branch("Y_ISOLATION_PX", &Y_ISOLATION_PX_out);
Float_t Y_ISOLATION_PY_out;
output.Branch("Y_ISOLATION_PY", &Y_ISOLATION_PY_out);
Float_t Y_ISOLATION_PZ_out;
output.Branch("Y_ISOLATION_PZ", &Y_ISOLATION_PZ_out);
Float_t Y_ISOLATION_PIDK_out;
output.Branch("Y_ISOLATION_PIDK", &Y_ISOLATION_PIDK_out);
Float_t Y_ISOLATION_PIDp_out;
output.Branch("Y_ISOLATION_PIDp", &Y_ISOLATION_PIDp_out);
Float_t Y_ISOLATION_NNk_out;
output.Branch("Y_ISOLATION_NNk", &Y_ISOLATION_NNk_out);
Float_t Y_ISOLATION_NNpi_out;
output.Branch("Y_ISOLATION_NNpi", &Y_ISOLATION_NNpi_out);
Float_t Y_ISOLATION_NNp_out;
output.Branch("Y_ISOLATION_NNp", &Y_ISOLATION_NNp_out);
Float_t Y_ISOLATION_IsMuon_out;
output.Branch("Y_ISOLATION_IsMuon", &Y_ISOLATION_IsMuon_out);
Float_t Y_ISOLATION_NNghost_out;
output.Branch("Y_ISOLATION_NNghost", &Y_ISOLATION_NNghost_out);
Int_t Y_ISOLATION_TRUEID_out;
output.Branch("Y_ISOLATION_TRUEID", &Y_ISOLATION_TRUEID_out);
Double_t Y_ISOLATION_CHI22_out;
output.Branch("Y_ISOLATION_CHI22", &Y_ISOLATION_CHI22_out);
Int_t Y_ISOLATION_SC2_out;
output.Branch("Y_ISOLATION_SC2", &Y_ISOLATION_SC2_out);
Double_t Y_ISOLATION_ANGLE2_out;
output.Branch("Y_ISOLATION_ANGLE2", &Y_ISOLATION_ANGLE2_out);
Double_t Y_ISOLATION_BDT2_out;
output.Branch("Y_ISOLATION_BDT2", &Y_ISOLATION_BDT2_out);
Float_t Y_ISOLATION_CHARGE2_out;
output.Branch("Y_ISOLATION_CHARGE2", &Y_ISOLATION_CHARGE2_out);
Float_t Y_ISOLATION_Type2_out;
output.Branch("Y_ISOLATION_Type2", &Y_ISOLATION_Type2_out);
Float_t Y_ISOLATION_PE2_out;
output.Branch("Y_ISOLATION_PE2", &Y_ISOLATION_PE2_out);
Float_t Y_ISOLATION_PX2_out;
output.Branch("Y_ISOLATION_PX2", &Y_ISOLATION_PX2_out);
Float_t Y_ISOLATION_PY2_out;
output.Branch("Y_ISOLATION_PY2", &Y_ISOLATION_PY2_out);
Float_t Y_ISOLATION_PZ2_out;
output.Branch("Y_ISOLATION_PZ2", &Y_ISOLATION_PZ2_out);
Float_t Y_ISOLATION_PIDK2_out;
output.Branch("Y_ISOLATION_PIDK2", &Y_ISOLATION_PIDK2_out);
Float_t Y_ISOLATION_PIDp2_out;
output.Branch("Y_ISOLATION_PIDp2", &Y_ISOLATION_PIDp2_out);
Float_t Y_ISOLATION_NNk2_out;
output.Branch("Y_ISOLATION_NNk2", &Y_ISOLATION_NNk2_out);
Float_t Y_ISOLATION_NNpi2_out;
output.Branch("Y_ISOLATION_NNpi2", &Y_ISOLATION_NNpi2_out);
Float_t Y_ISOLATION_NNp2_out;
output.Branch("Y_ISOLATION_NNp2", &Y_ISOLATION_NNp2_out);
Float_t Y_ISOLATION_IsMuon2_out;
output.Branch("Y_ISOLATION_IsMuon2", &Y_ISOLATION_IsMuon2_out);
Float_t Y_ISOLATION_NNghost2_out;
output.Branch("Y_ISOLATION_NNghost2", &Y_ISOLATION_NNghost2_out);
Int_t Y_ISOLATION_TRUEID2_out;
output.Branch("Y_ISOLATION_TRUEID2", &Y_ISOLATION_TRUEID2_out);
Double_t Y_ISOLATION_CHI23_out;
output.Branch("Y_ISOLATION_CHI23", &Y_ISOLATION_CHI23_out);
Int_t Y_ISOLATION_SC3_out;
output.Branch("Y_ISOLATION_SC3", &Y_ISOLATION_SC3_out);
Double_t Y_ISOLATION_BDT3_out;
output.Branch("Y_ISOLATION_BDT3", &Y_ISOLATION_BDT3_out);
Double_t Y_ISOLATION_ANGLE3_out;
output.Branch("Y_ISOLATION_ANGLE3", &Y_ISOLATION_ANGLE3_out);
Float_t Y_ISOLATION_CHARGE3_out;
output.Branch("Y_ISOLATION_CHARGE3", &Y_ISOLATION_CHARGE3_out);
Float_t Y_ISOLATION_Type3_out;
output.Branch("Y_ISOLATION_Type3", &Y_ISOLATION_Type3_out);
Float_t Y_ISOLATION_PE3_out;
output.Branch("Y_ISOLATION_PE3", &Y_ISOLATION_PE3_out);
Float_t Y_ISOLATION_PX3_out;
output.Branch("Y_ISOLATION_PX3", &Y_ISOLATION_PX3_out);
Float_t Y_ISOLATION_PY3_out;
output.Branch("Y_ISOLATION_PY3", &Y_ISOLATION_PY3_out);
Float_t Y_ISOLATION_PZ3_out;
output.Branch("Y_ISOLATION_PZ3", &Y_ISOLATION_PZ3_out);
Float_t Y_ISOLATION_PIDK3_out;
output.Branch("Y_ISOLATION_PIDK3", &Y_ISOLATION_PIDK3_out);
Float_t Y_ISOLATION_PIDp3_out;
output.Branch("Y_ISOLATION_PIDp3", &Y_ISOLATION_PIDp3_out);
Float_t Y_ISOLATION_NNk3_out;
output.Branch("Y_ISOLATION_NNk3", &Y_ISOLATION_NNk3_out);
Float_t Y_ISOLATION_NNpi3_out;
output.Branch("Y_ISOLATION_NNpi3", &Y_ISOLATION_NNpi3_out);
Float_t Y_ISOLATION_NNp3_out;
output.Branch("Y_ISOLATION_NNp3", &Y_ISOLATION_NNp3_out);
Float_t Y_ISOLATION_IsMuon3_out;
output.Branch("Y_ISOLATION_IsMuon3", &Y_ISOLATION_IsMuon3_out);
Float_t Y_ISOLATION_NNghost3_out;
output.Branch("Y_ISOLATION_NNghost3", &Y_ISOLATION_NNghost3_out);
Int_t Y_ISOLATION_TRUEID3_out;
output.Branch("Y_ISOLATION_TRUEID3", &Y_ISOLATION_TRUEID3_out);
Double_t Y_ISOLATION_CHI24_out;
output.Branch("Y_ISOLATION_CHI24", &Y_ISOLATION_CHI24_out);
Int_t Y_ISOLATION_SC4_out;
output.Branch("Y_ISOLATION_SC4", &Y_ISOLATION_SC4_out);
Double_t Y_ISOLATION_BDT4_out;
output.Branch("Y_ISOLATION_BDT4", &Y_ISOLATION_BDT4_out);
Double_t Y_ISOLATION_ANGLE4_out;
output.Branch("Y_ISOLATION_ANGLE4", &Y_ISOLATION_ANGLE4_out);
Float_t Y_ISOLATION_CHARGE4_out;
output.Branch("Y_ISOLATION_CHARGE4", &Y_ISOLATION_CHARGE4_out);
Float_t Y_ISOLATION_Type4_out;
output.Branch("Y_ISOLATION_Type4", &Y_ISOLATION_Type4_out);
Float_t Y_ISOLATION_PE4_out;
output.Branch("Y_ISOLATION_PE4", &Y_ISOLATION_PE4_out);
Float_t Y_ISOLATION_PX4_out;
output.Branch("Y_ISOLATION_PX4", &Y_ISOLATION_PX4_out);
Float_t Y_ISOLATION_PY4_out;
output.Branch("Y_ISOLATION_PY4", &Y_ISOLATION_PY4_out);
Float_t Y_ISOLATION_PZ4_out;
output.Branch("Y_ISOLATION_PZ4", &Y_ISOLATION_PZ4_out);
Float_t Y_ISOLATION_PIDK4_out;
output.Branch("Y_ISOLATION_PIDK4", &Y_ISOLATION_PIDK4_out);
Float_t Y_ISOLATION_PIDp4_out;
output.Branch("Y_ISOLATION_PIDp4", &Y_ISOLATION_PIDp4_out);
Float_t Y_ISOLATION_NNk4_out;
output.Branch("Y_ISOLATION_NNk4", &Y_ISOLATION_NNk4_out);
Float_t Y_ISOLATION_NNpi4_out;
output.Branch("Y_ISOLATION_NNpi4", &Y_ISOLATION_NNpi4_out);
Float_t Y_ISOLATION_NNp4_out;
output.Branch("Y_ISOLATION_NNp4", &Y_ISOLATION_NNp4_out);
Float_t Y_ISOLATION_IsMuon4_out;
output.Branch("Y_ISOLATION_IsMuon4", &Y_ISOLATION_IsMuon4_out);
Float_t Y_ISOLATION_NNghost4_out;
output.Branch("Y_ISOLATION_NNghost4", &Y_ISOLATION_NNghost4_out);
Int_t Y_ISOLATION_TRUEID4_out;
output.Branch("Y_ISOLATION_TRUEID4", &Y_ISOLATION_TRUEID4_out);


  while (reader.Next()) {
    
    Y_OWNPV_X_out = (*Y_OWNPV_X);
Y_OWNPV_Y_out = (*Y_OWNPV_Y);
Y_OWNPV_Z_out = (*Y_OWNPV_Z);
Y_OWNPV_XERR_out = (*Y_OWNPV_XERR);
Y_OWNPV_YERR_out = (*Y_OWNPV_YERR);
Y_OWNPV_ZERR_out = (*Y_OWNPV_ZERR);
Y_OWNPV_CHI2_out = (*Y_OWNPV_CHI2);
Y_OWNPV_NDOF_out = (*Y_OWNPV_NDOF);
Y_ISOLATION_CHI2_out = (*Y_ISOLATION_CHI2);
Y_ISOLATION_ANGLE_out = (*Y_ISOLATION_ANGLE);
Y_ISOLATION_SC_out = (*Y_ISOLATION_SC);
Y_ISOLATION_BDT_out = (*Y_ISOLATION_BDT);
Y_ISOLATION_CHARGE_out = (*Y_ISOLATION_CHARGE);
Y_ISOLATION_Type_out = (*Y_ISOLATION_Type);
Y_ISOLATION_PE_out = (*Y_ISOLATION_PE);
Y_ISOLATION_PX_out = (*Y_ISOLATION_PX);
Y_ISOLATION_PY_out = (*Y_ISOLATION_PY);
Y_ISOLATION_PZ_out = (*Y_ISOLATION_PZ);
Y_ISOLATION_PIDK_out = (*Y_ISOLATION_PIDK);
Y_ISOLATION_PIDp_out = (*Y_ISOLATION_PIDp);
Y_ISOLATION_NNk_out = (*Y_ISOLATION_NNk);
Y_ISOLATION_NNpi_out = (*Y_ISOLATION_NNpi);
Y_ISOLATION_NNp_out = (*Y_ISOLATION_NNp);
Y_ISOLATION_IsMuon_out = (*Y_ISOLATION_IsMuon);
Y_ISOLATION_NNghost_out = (*Y_ISOLATION_NNghost);
Y_ISOLATION_TRUEID_out = (*Y_ISOLATION_TRUEID);
Y_ISOLATION_CHI22_out = (*Y_ISOLATION_CHI22);
Y_ISOLATION_SC2_out = (*Y_ISOLATION_SC2);
Y_ISOLATION_ANGLE2_out = (*Y_ISOLATION_ANGLE2);
Y_ISOLATION_BDT2_out = (*Y_ISOLATION_BDT2);
Y_ISOLATION_CHARGE2_out = (*Y_ISOLATION_CHARGE2);
Y_ISOLATION_Type2_out = (*Y_ISOLATION_Type2);
Y_ISOLATION_PE2_out = (*Y_ISOLATION_PE2);
Y_ISOLATION_PX2_out = (*Y_ISOLATION_PX2);
Y_ISOLATION_PY2_out = (*Y_ISOLATION_PY2);
Y_ISOLATION_PZ2_out = (*Y_ISOLATION_PZ2);
Y_ISOLATION_PIDK2_out = (*Y_ISOLATION_PIDK2);
Y_ISOLATION_PIDp2_out = (*Y_ISOLATION_PIDp2);
Y_ISOLATION_NNk2_out = (*Y_ISOLATION_NNk2);
Y_ISOLATION_NNpi2_out = (*Y_ISOLATION_NNpi2);
Y_ISOLATION_NNp2_out = (*Y_ISOLATION_NNp2);
Y_ISOLATION_IsMuon2_out = (*Y_ISOLATION_IsMuon2);
Y_ISOLATION_NNghost2_out = (*Y_ISOLATION_NNghost2);
Y_ISOLATION_TRUEID2_out = (*Y_ISOLATION_TRUEID2);
Y_ISOLATION_CHI23_out = (*Y_ISOLATION_CHI23);
Y_ISOLATION_SC3_out = (*Y_ISOLATION_SC3);
Y_ISOLATION_BDT3_out = (*Y_ISOLATION_BDT3);
Y_ISOLATION_ANGLE3_out = (*Y_ISOLATION_ANGLE3);
Y_ISOLATION_CHARGE3_out = (*Y_ISOLATION_CHARGE3);
Y_ISOLATION_Type3_out = (*Y_ISOLATION_Type3);
Y_ISOLATION_PE3_out = (*Y_ISOLATION_PE3);
Y_ISOLATION_PX3_out = (*Y_ISOLATION_PX3);
Y_ISOLATION_PY3_out = (*Y_ISOLATION_PY3);
Y_ISOLATION_PZ3_out = (*Y_ISOLATION_PZ3);
Y_ISOLATION_PIDK3_out = (*Y_ISOLATION_PIDK3);
Y_ISOLATION_PIDp3_out = (*Y_ISOLATION_PIDp3);
Y_ISOLATION_NNk3_out = (*Y_ISOLATION_NNk3);
Y_ISOLATION_NNpi3_out = (*Y_ISOLATION_NNpi3);
Y_ISOLATION_NNp3_out = (*Y_ISOLATION_NNp3);
Y_ISOLATION_IsMuon3_out = (*Y_ISOLATION_IsMuon3);
Y_ISOLATION_NNghost3_out = (*Y_ISOLATION_NNghost3);
Y_ISOLATION_TRUEID3_out = (*Y_ISOLATION_TRUEID3);
Y_ISOLATION_CHI24_out = (*Y_ISOLATION_CHI24);
Y_ISOLATION_SC4_out = (*Y_ISOLATION_SC4);
Y_ISOLATION_BDT4_out = (*Y_ISOLATION_BDT4);
Y_ISOLATION_ANGLE4_out = (*Y_ISOLATION_ANGLE4);
Y_ISOLATION_CHARGE4_out = (*Y_ISOLATION_CHARGE4);
Y_ISOLATION_Type4_out = (*Y_ISOLATION_Type4);
Y_ISOLATION_PE4_out = (*Y_ISOLATION_PE4);
Y_ISOLATION_PX4_out = (*Y_ISOLATION_PX4);
Y_ISOLATION_PY4_out = (*Y_ISOLATION_PY4);
Y_ISOLATION_PZ4_out = (*Y_ISOLATION_PZ4);
Y_ISOLATION_PIDK4_out = (*Y_ISOLATION_PIDK4);
Y_ISOLATION_PIDp4_out = (*Y_ISOLATION_PIDp4);
Y_ISOLATION_NNk4_out = (*Y_ISOLATION_NNk4);
Y_ISOLATION_NNpi4_out = (*Y_ISOLATION_NNpi4);
Y_ISOLATION_NNp4_out = (*Y_ISOLATION_NNp4);
Y_ISOLATION_IsMuon4_out = (*Y_ISOLATION_IsMuon4);
Y_ISOLATION_NNghost4_out = (*Y_ISOLATION_NNghost4);
Y_ISOLATION_TRUEID4_out = (*Y_ISOLATION_TRUEID4);

output.Fill();
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