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
      name = "boued";
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
      program = "${entrypoint}/bin/boued";
    };

    service = {
      lib,
      config,
      ...
    }: let
      cfg = config.services.boued;
    in {
      options.services.boued = {
        enable = lib.mkEnableOption "Boued backend app";

        databaseUrl = lib.mkOption {
          type = lib.types.str;
          default = "sqlite:////var/lib/boued/data.db";
          description = "Database URL used by the Boued backend";
        };

        port = lib.mkOption {
          type = lib.types.port;
          default = 6001;
          description = "Port the backend server will listen on.";
        };

        secretKeyFile = lib.mkOption {
          type = lib.types.path;
          default = "/var/lib/boued/secret.key";
          description = ''
            Path to the file containing the JWT secret key used by the backend.
          '';
        };

        admin = {
          username = lib.mkOption {
            type = lib.types.str;
            default = "admin";
            description = "First admin user name";
          };
          password = lib.mkOption {
            type = lib.types.str;
            default = "changeme";
            description = "First admin user password";
          };
        };
      };

      config = lib.mkIf cfg.enable {
        users.users.boued = {
          isSystemUser = true;
          group = "boued";
          home = "/var/lib/boued";
          createHome = true;
        };
        users.groups.boued = {};

        systemd.services.boued = {
          description = "Boued backend service";
          wantedBy = ["multi-user.target"];
          after = ["network.target"];

          environment = {
            DATABASE_URL = cfg.databaseUrl;
            SECRET_KEY_FILE = cfg.secretKeyFile;
            FIRST_USER_NAME = cfg.admin.username;
            FIRST_USER_PASSWORD = cfg.admin.password;
          };

          serviceConfig = {
            ExecStart = "${entrypoint}/bin/boued";
            WorkingDirectory = "/var/lib/boued";
            User = "boued";
            Group = "boued";
            StateDirectory = "boued";
            Restart = "on-failure";

            # Security hardening
            CapabilityBoundingSet = "";
            RestrictAddressFamilies = "AF_UNIX AF_INET AF_INET6";
            SystemCallFilter = "~@clock @cpu-emulation @keyring @module @obsolete @raw-io @reboot @swap @resources @privileged @mount @debug";
            NoNewPrivileges = "yes";
            ProtectClock = "yes";
            ProtectKernelLogs = "yes";
            ProtectControlGroups = "yes";
            ProtectKernelModules = "yes";
            SystemCallArchitectures = "native";
            RestrictNamespaces = "yes";
            RestrictSUIDSGID = "yes";
            ProtectHostname = "yes";
            ProtectKernelTunables = "yes";
            RestrictRealtime = "yes";
            ProtectProc = "invisible";
            PrivateUsers = "yes";
            LockPersonality = "yes";
            UMask = "0077";
            RemoveIPC = "yes";
            LimitCORE = "0";
            ProtectHome = "yes";
            PrivateTmp = "yes";
            ProtectSystem = "strict";
            ProcSubset = "pid";
            SocketBindAllow = ["tcp:${builtins.toString cfg.port}"];
            SocketBindDeny = "any";

            LimitNOFILE = 1024;
            LimitNPROC = 64;
            MemoryMax = "100M";
          };
        };
      };
    };
  in {
    packages.${system} = {
      frontend = frontend;
      default = backend;
    };
    apps.${system}.default = app;
    devShells.${system}.default = shell;
    nixosModules.pleustradenn-service = service;
  };
}
