{
  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-25.05";

  outputs = {nixpkgs, ...}: let
    system = "x86_64-linux";
    pkgs = import nixpkgs {inherit system;};

    pythonPackages = ps:
      with ps; [
        fastapi
        uvicorn
        sqlmodel
        websockets
        pyjwt
        python-multipart
        bcrypt
      ];
    pythonEnv = pkgs.python313.withPackages pythonPackages;

    frontend = pkgs.buildNpmPackage {
      pname = "frontend";
      version = "2.0.0";
      npmDepsHash = "sha256-yzKB8QQibLu4wUqeBToK/ChVviODBl3AQXrmQ6eh+08=";
      src = ./frontend;
      installPhase = ''
        runHook preInstall
        cp -r build $out/
        runHook postInstall
      '';
    };

    backend = pkgs.stdenv.mkDerivation {
      name = "boued-app";
      src = pkgs.lib.cleanSource ./backend;
      buildInputs = [pythonEnv];

      installPhase = ''
        mkdir -p $out/backend/static
        cp -r . $out/backend/
        cp -r ${frontend}/* $out/backend/static/
      '';

      meta.mainProgram = "run";
    };

    entrypoint = pkgs.writeShellApplication {
      name = "boued-run";
      runtimeInputs = [pythonEnv];
      text = ''
        export PYTHONPATH=${backend}/backend
        cd ${backend}
        exec ${pythonEnv}/bin/uvicorn backend.main:app --proxy-headers --host 0.0.0.0 --port 6001
      '';
    };

    shell = pkgs.mkShell {
      buildInputs = [
        pythonEnv
        pkgs.nodejs_24
        pkgs.sqlite
      ];
    };

    app = {
      type = "app";
      program = "${entrypoint}/bin/boued-run";
    };
  in {
    packages.${system} = {
      frontend = frontend;
      default = backend;
    };
    apps.${system}.default = app;
    devShells.${system}.default = shell;
  };
}
