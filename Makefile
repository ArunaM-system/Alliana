.PHONY: help dev test migrate clean

help:
	@echo "ALLINA Platform Build and Execution Commands:"
	@echo "  make dev      - Start all services with Docker Compose"
	@echo "  make test     - Run backend test suite"
	@echo "  make migrate  - Run database migrations"
	@echo "  make clean    - Remove cached files and containers"

dev:
	docker compose up --build

test:
	pytest backend/tests

migrate:
	cd backend && alembic upgrade head

clean:
	docker compose down
