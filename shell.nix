{ pkgs ? import <nixpkgs> {} }:

with pkgs;

mkShell {
  name = "FoxDot";
  buildInputs = [ (callPackage ./. {}) ];
}