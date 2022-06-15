{
  description = "Python babymaker (flat ntuple generation tool) library.";

  inputs = {
    root-curated.url = "github:umd-lhcb/root-curated";
    nixpkgs.follows = "root-curated/nixpkgs";
    flake-utils.follows = "root-curated/flake-utils";
  };

  outputs = { self, root-curated, nixpkgs, flake-utils }:
    {
      overlay = import ./nix/overlay.nix;
    }
    //
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ root-curated.overlay ];
        };
        python = pkgs.python3;
        pythonPackages = python.pkgs;
      in
      {
        # packages = flake-utils.lib.flattenTree {
        #   pyBabyMaker = python.withPackages (p: with p; [ pyBabyMaker ]);
        # };
        devShell = pkgs.mkShell rec {
          name = "pyBabyMaker-dev";
          buildInputs = with pythonPackages; [
            pkgs.root
            pytest

            # Dev tools
            jedi
            flake8
            pylint
            virtualenvwrapper

            # Pinned Python dependencies
            numpy
            uproot
            lz4
            pyyaml
            lark-parser
          ];

          shellHook = ''
            # Allow the use of wheels.
            SOURCE_DATE_EPOCH=$(date +%s)

            if test -d $HOME/build/python-venv; then
              VENV=$HOME/build/python-venv/${name}
            else
              VENV=./.virtualenv
            fi

            if test ! -d $VENV; then
              virtualenv $VENV
            fi
            source $VENV/bin/activate

            # allow for the environment to pick up packages installed with virtualenv
            export PYTHONPATH=$VENV/${python.sitePackages}/:$PYTHONPATH

            # fix libstdc++.so not found error
            export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH
          '';
        };
      });
}
