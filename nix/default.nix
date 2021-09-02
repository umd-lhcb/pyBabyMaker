{ stdenv
, buildPythonPackage
, uproot
, pyyaml
, lark-parser
}:

# FIXME: We require uproot 4 but it's not in nixpkgs yet.

buildPythonPackage rec {
  pname = "pyBabyMaker";
  version = "0.4.0";

  src = builtins.path { path = ./..; name = pname; };

  propagatedBuildInputs = [
    uproot
    pyyaml
    lark-parser
  ];

  doCheck = false;
}
