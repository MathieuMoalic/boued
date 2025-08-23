# Boued

A small, self-hostable web app to manage groceries and shopping lists — built with **SvelteKit**, **TypeScript**, **Prisma**, **SQLite (by default)**, TailwindCSS, Vite, and a Nix flake for reproducible dev. ([GitHub][1])

![Screenshots](./screenshots.png) ([GitHub][1])

## Features

* Fast, minimal grocery list management
* Add/mark items, quick search, and lightweight categorization
* Keyboard-friendly UI
* Works great locally or behind a home server reverse proxy
* SQLite out of the box; switchable to other databases via Prisma

## Tech stack

* **Frontend/Server**: SvelteKit + Vite + TypeScript
* **ORM & DB**: Prisma with a default SQLite DB
* **Styling**: TailwindCSS
* **Dev env**: Nix flake

## Quick start

### 1) Clone

```bash
git clone https://github.com/MathieuMoalic/boued
cd boued
```

### 2) Configure environment

Create a `.env` file in the repo root:

```ini
# Prisma connection string (SQLite by default)
DATABASE_URL="file:./dev.db"

# Optional: change the dev server port
PORT=5173

# Optional: CORS/allowed origin in prod (adjust for your domain)
ORIGIN="http://localhost:5173"
```

### 3) Install dependencies

```bash
npm install
```

If you use **Nix**:

```bash
nix develop
npm install
```

### 4) Setup the database

```bash
npx prisma generate
npx prisma migrate dev --name init
```

### 5) Run in development

```bash
npm run dev
# then open the printed URL (http://localhost:5173)
```


## Build & run (production)

```bash
nix run .
```

> When deploying, run **database migrations** in your release step:
>
> ```bash
> npx prisma migrate deploy
> ```


## Deployment tips
As a nixos module:

Add in flake.nix inputs:
```nix
boued.url = "github:MathieuMoalic/boued";
```

Using with caddy:
```nix
{...}: let
  port = 10025;
in {
  services.caddy = {
    virtualHosts = {
      "boued.matmoa.eu" = {
        extraConfig = ''
          reverse_proxy localhost:${toString port}
        '';
      };
    };
  };
  services.boued = {
    enable = true;
    port = port;
  };
}

```

## License

GPL-3.0 — see [`LICENSE`](./LICENSE). ([GitHub][1])
