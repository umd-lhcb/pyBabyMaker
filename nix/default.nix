{ stdenv
, buildPythonPackage
, root
, pyyaml
, lark-parser
}:

buildPythonPackage rec {
  pname = "pyBabyMaker";
  version = "0.3.4";

  src = builtins.path { path = ./..; name = pname; };

  buildInputs = [ root ];
  propagatedBuildInputs = [
    pyyaml
    lark-parser
  ];

  doCheck = false;
}
