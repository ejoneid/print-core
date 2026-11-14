{
  description = "Rust development shell";

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
      in
      {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            rustc
            cargo
            rustfmt
            clippy
            rust-analyzer

            # Nice-to-haves
            bacon # background checker: re-runs check/clippy/test on save
            cargo-watch # run any cargo command on file changes
            cargo-edit # cargo add / rm / upgrade helpers
          ];

          # Lets rust-analyzer find the standard library sources
          RUST_SRC_PATH = "${pkgs.rustPlatform.rustLibSrc}";

          # Full backtraces when something panics
          RUST_BACKTRACE = "1";
        };
      }
    );
}
