# Deploying

Meilisearch doesn't have to be accessible from the internet, only the backend server needs to reach it.

## podman or docker:

```bash
podman run -d \
    --name groceries \
    -e MEILI_URL=localhost:7700 \
    -e MEILI_KEY=CHANGE_ME \
    -p 6001:6001 \
    -v $(pwd)/data:/data:z \
    ghcr.io/mathieumoalic/groceries-app:3.1.1

podman run -d \
    --name groceries-meilisearch \
    -e MEILI_MASTER_KEY=CHANGE_ME \
    -e MEILI_ENV=production \
    -e MEILI_NO_ANALYTICS \
    -p 7700:7700 \
    -v $(pwd)/meili_data:/meili_data:z \
    docker.io/getmeili/meilisearch:v1.2.0
```
## docker-compose

```yml
services:
  groceries:
    image: ghcr.io/mathieumoalic/groceries-app:3.1.1
    container_name: groceries
    environment:
      - MEILI_URL=${MEILI_URL}
      - MEILI_KEY=${MEILI_KEY}
    ports:
      - 6001:6001
    volumes:
      - ./data:/data:z

  groceries-meilisearch:
    image: docker.io/getmeili/meilisearch:v1.2.0
    container_name: groceries-meilisearch
    environment:
      - MEILI_MASTER_KEY=${MEILI_KEY}
      - MEILI_ENV=production
      - MEILI_NO_ANALYTICS
    ports:
      - 6002:7700
    volumes:
      - ./meili_data:/meili_data:z
```
With `.env` :
```bash
MEILI_URL="http://localhost:6002"
MEILI_KEY="CHANGE_ME"
```
## Reverse proxy
### Caddy
```Caddyfile
groceries.example.com {
	reverse_proxy localhost:6001
}
```

## Dev

`just dev` starts the hot-reload svelte frontend and fastapi backend as well as the meilisearch, all in containers

Proxying the dev stack with caddy:

```
groceries-dev.example.com {
	reverse_proxy /api groceries-backend-dev:6001
	reverse_proxy /api/* groceries-backend-dev:6001
	reverse_proxy groceries-frontend-dev:6000
}
```