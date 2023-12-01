{
  description = "Development Shell for Python AWS CDK Repos";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem
      ( system:
        let 
          pkgs = import nixpkgs { inherit system; };
        in
        with pkgs;
        {
          devShells.default = mkShell {
            buildInputs = [
              poetry
              python311
              python311Packages.jedi
              nodejs
              awscli2
            ];

            shellHook = ''
              alias cdk="npx aws-cdk"
            '';
          };
        }
      );
}
