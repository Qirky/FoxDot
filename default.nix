{ lib, pkgs ? import <nixpkgs> { } }:

with pkgs.python310Packages;

buildPythonPackage rec {
  name = "FoxDot";
  version = "0.1";
  src = ./.;
  propagatedBuildInputs = [ setuptools wheel tkinter ];
  pythonImportsCheck = [ "FoxDot" ];
  doCheck = false;

  meta = with lib; {
    description = "Our FoxDot clone";
    homepage = "https://github.com/UTCSheffield/FoxDot";
    maintainers = with maintainers; [ devramsean0 ];
  };
}