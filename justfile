set dotenv-load

front-dev:
	podman run -it --rm \
		--name='groceries-frontend-dev' \
		-p 6000:6000 \
		-v ./frontend:/app:z \
		--workdir=/app \
		node:20.3.0-alpine3.18 \
		sh  

back-dev:
	podman run -it --rm \
		--name='groceries-backend-dev' \
		-p 6001:6001 \
		-v ./backend:/app:z \
		-e MEILI_URL=$MEILI_URL \
		-e MEILI_KEY=$MEILI_KEY \
		--workdir=/app \
		python:3.11 \
		sh -c "pip -q install fastapi meilisearch uvicorn && uvicorn main:app --proxy-headers --host 0.0.0.0 --port 6001 --reload"

search-dev:
	podman run -it --rm \
		--name='groceries-meilisearch' \
		-p 6002:7700 \
		-v ./meili_data:/meili_data:z \
		-e MEILI_MASTER_KEY=3982r7t5gruef09248g379ruocnije802g97yiv \
		-e MEILI_ENV=development \
		getmeili/meilisearch:v1.2.0

prod:
	podman build -t localhost/matmoa/groceries:v3 .

