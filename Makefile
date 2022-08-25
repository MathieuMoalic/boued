dev:
	docker-compose -p "groceries-app-dev" -f "docker-compose.dev.yml" up -d --build
prod:
	docker-compose -p "groceries-app-prod" -f "docker-compose.prod.yml" up -d --build