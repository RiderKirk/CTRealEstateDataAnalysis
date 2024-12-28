{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python3
    pkgs.python3Packages.jupyterlab 
    pkgs.python3Packages.pandas
    pkgs.python3Packages.matplotlib
    pkgs.python3Packages.numpy
    pkgs.python3Packages.seaborn
    pkgs.python3Packages.folium
  ];
}
