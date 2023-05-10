dev:
	docker-compose -p "groceries-app-dev" -f "docker-compose.dev.yml" up -d --build

prod:
	cd backend && podman build -t localhost/matmoa/groceries-backend -f prod.Dockerfile .
	cd ..
	cd frontend && podman build -t localhost/matmoa/groceries-frontend -f prod.Dockerfile .