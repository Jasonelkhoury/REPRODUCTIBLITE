let
  rev = "9f78f44a87948854445dae0b6bf82b2e87e4efb5";
  sha256 = "1359snxlhm0z1d83c45q3b2r7fpa53bimjnvr4h160i0q0l4fvmc";
in
import (builtins.fetchTarball {
  url = "https://github.com/NixOS/nixpkgs/archive/${rev}.tar.gz";
  inherit sha256;
})
