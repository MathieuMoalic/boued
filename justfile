set dotenv-load

dev: front-dev back-dev search-dev

clean:
    podman rm --force groceries-frontend-dev groceries-backend-dev groceries-meilisearch-dev

code-server-dev:
    podman run -d \
        --network tmp-proxy \
        --name groceries-code-server \
        -v .:/home/coder/project:z \
        -v .dev/code-server/config:/root/.config/code-server:z \
        -v .dev/code-server/cache:/root/.local/share/code-server:z \
        -u "0:0" \
        -e "DOCKER_USER=root" \
        docker.io/codercom/code-server:latest \
        code-server --auth=none

front-dev:
    podman run -d \
        --network tmp-proxy \
        --name groceries-frontend-dev \
        -v ./frontend:/app:z \
        --workdir=/app \
        node:20.3.0-alpine3.18 \
        sh -c "npm i && npm run dev"

front-dev-it:
    podman run --rm -it \
        --network tmp-proxy \
        --name groceries-frontend-dev \
        -v ./frontend:/app:z \
        --workdir=/app \
        node:20.3.0-alpine3.18 sh

back-dev:
    podman run -d \
        --network tmp-proxy \
        --name groceries-backend-dev \
        -v ./backend:/app:z \
        -v .dev/backend:/data:z \
        -e MEILI_URL=http://groceries-meilisearch-dev:7700 \
        -e DEV=True \
        --workdir=/app \
        python:3.11-slim \
        sh -c "pip install -r requirements.txt && uvicorn main:app --proxy-headers --host 0.0.0.0 --port 6001 --reload"
back-dev-it:
    podman run --rm -it \
        --network tmp-proxy \
        --name groceries-backend-dev \
        -v ./backend:/app:z \
        -v .dev/backend:/data:z \
        -e MEILI_URL=http://groceries-meilisearch-dev:7700 \
        -e DEV=True \
        --workdir=/app \
        python:3.11-slim \
        bash

search-dev:
    mkdir -p .dev/meili_data
    podman run -d \
        --network tmp-proxy \
        --name groceries-meilisearch-dev \
        -v .dev/meili_data:/meili_data:z \
        -e MEILI_ENV=development \
        docker.io/getmeili/meilisearch:v1.2.0

staging: clean-staging
    podman build -t localhost/groceries-staging:latest .

    podman network create groceries-staging

    podman run -d --replace \
        --name groceries-meilisearch-staging \
        --network groceries-staging \
        -e MEILI_MASTER_KEY=GUw5MX4OIu6kpPZp1DQQV-tsjud2Pjk5NcfNj0VQwLU \
        -e MEILI_ENV=production \
        -e MEILI_NO_ANALYTICS \
        docker.io/getmeili/meilisearch:v1.2.0

    podman run -d --replace \
        --name groceries-staging \
        --network tmp-proxy \
        --network groceries-staging \
        --requires groceries-meilisearch-staging \
        -v .dev/data:/data:z \
        -e MEILI_URL=http://groceries-meilisearch-staging:7700 \
        -e MEILI_KEY=GUw5MX4OIu6kpPZp1DQQV-tsjud2Pjk5NcfNj0VQwLU \
        localhost/groceries-staging:latest


clean-staging:
    podman rm -f groceries-staging 
    podman rm -f groceries-meilisearch-staging
    podman network remove -f groceries-staging
    podman image rm localhost/groceries-staging:latest

tag-release:
    git add .
    git commit -m "v$(jq -r .version frontend/package.json)"
    git tag "v$(jq -r .version frontend/package.json)"
    git push