# 🛒 Boued

A simple, self-hostable web app to manage groceries and shopping lists, built with a FastAPI backend and a SvelteKit frontend.

![App Preview](./screenshots.png)

---

## 🧰 Features

- Real-time grocery list management
- Item categories and notes
- Search and toggle active/inactive items
- WebSocket-based sync
- Authenticated access
- SvelteKit + FastAPI + SQLite

---

## 🧱 Project Structure

- `backend/`: FastAPI backend, models, routes, and WebSocket
- `frontend/`: SvelteKit app
- REST API exposed under `/api`

---

## 📦 Deployment

### Using Podman or Docker

```bash
podman run -d --replace \
	--name groceries \
	--network groceries-proxy \
	-v ./groceries:/data \
	-e ADMIN_USERNAME=${ADMIN_USERNAME} \
	-e ADMIN_PASSWORD=${ADMIN_PASSWORD} \
	ghcr.io/mathieumoalic/groceries-app:latest
```

---

### 🔁 Reverse Proxy (Caddy)

```Caddyfile
groceries.example.com {
	reverse_proxy localhost:6001
}
```

---

## ⚙️ Stack

- **Backend**: Python, FastAPI, SQLModel, WebSocket
- **Frontend**: SvelteKit, TailwindCSS
- **DB**: SQLite
- **Auth**: JWT-based
- **Container**: Docker/Podman-ready

---

## 🧪 Development

```bash
# Backend
cd backend
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```
