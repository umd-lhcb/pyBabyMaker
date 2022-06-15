final: prev:

{
  python3 = prev.python3.override {
    packageOverrides = python-final: python-prev: {
      pyBabyMaker = python-final.callPackage ./default.nix { };
    };
  };
}
