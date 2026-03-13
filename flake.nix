{
  description = "Python 3.14 development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };
        python = pkgs.python314;
        claude = pkgs.claude-code;
      in
      {
        devShells.default = pkgs.mkShell {
          packages = [
            claude
            python
            pkgs.uv
            pkgs.pipx
          ];
        };
      }
    );
}
