all:
	cd frontend && docker build -t groceries-frontend .
	cd ..
	cd backend && docker build -t groceries-backend .
	cd ..
	docker-compose up -d