final: prev:
let
  pythonOverrides = {
    packageOverrides = self: super: {
      pyBabyMaker = self.callPackage ./default.nix { };
    };
  };
in
rec {
  python3 = prev.python3.override pythonOverrides;
  pythonPackages = python3.pkgs;
}
