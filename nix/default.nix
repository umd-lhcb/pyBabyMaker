{ stdenv
, buildPythonPackage
, pyyaml
, lark-parser
}:

buildPythonPackage rec {
  pname = "pyUTM";
  version = "0.3.3";

  src = builtins.path { path = ./..; name = pname; };

  propagatedBuildInputs = [
    pyyaml
    lark-parser
  ];

  doCheck = false;
}
