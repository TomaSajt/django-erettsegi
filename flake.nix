{
  outputs = { self, nixpkgs }:
    let
      pkgs = import nixpkgs { system = "x86_64-linux"; };
      python = (pkgs.python311.withPackages (ps: with ps; [ django ]));
    in
    {
      devShell.x86_64-linux = python.env;
    };
}

