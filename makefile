# Extract version and name from src/__init__.py using bash
VERSION := $(shell grep 'VERSION = ' src/__init__.py | sed 's/.*"\(.*\)".*/\1/')
NAME := $(shell grep 'NAME = ' src/__init__.py | sed 's/.*"\(.*\)".*/\1/')

# Docker commands (standalone)
docker-build:
	docker build -t $(NAME):$(VERSION) .

docker-run:
	docker run -p 8000:8000 $(NAME):$(VERSION)

docker-build-latest:
	docker build -t $(NAME):latest .

docker-run-latest:
	docker run -p 8000:8000 $(NAME):latest

# Docker Compose commands
compose-up:
	docker compose up -d --build

compose-down:
	docker compose down

run.app:
	uv run src/main.py