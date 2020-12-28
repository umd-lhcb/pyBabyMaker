{
  description = "Python babymaker (flat ntuple generation tool) library.";

  inputs = rec {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-20.09";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    {
      overlay = import ./nix/overlay.nix;
    }
    //
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ self.overlay ];
        };
        python = pkgs.python3;
        pythonPackages = python.pkgs;
        root = pkgs.root;
      in
      rec {
        packages = {
          pyBabyMakerEnv = pkgs.python3.withPackages (ps: with ps; [
            pyBabyMaker

            # Testing
            pytest

            # C++ wrapper generation
            cython
          ]);
        };

        devShell = packages.pyBabyMakerEnv.env;
      });
}
