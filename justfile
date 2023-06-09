dev:
	podman rm -f groceries-frontend-dev groceries-backend-dev
	DOCKER_HOST="unix://$XDG_RUNTIME_DIR/podman/podman.sock" docker-compose -p "groceries-app-dev" -f "docker-compose.dev.yml" up --build

prod:
	cd backend && podman build -t localhost/matmoa/groceries-backend -f prod.Dockerfile .
	cd ..
	cd frontend && podman build -t localhost/matmoa/groceries-frontend -f prod.Dockerfile .