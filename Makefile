APP_NAME=instahyre_coding_task_api
DOCKER_COMPOSE_FILE=docker-compose.yml
FLASK_ENV=grep FLASK_ENV .env | cut -d '=' -f2
FLASK_APP=run.py
DB_SERVICE=db
WEB_SERVICE=web
REDIS_SERVICE=redis

.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  build            Build the docker images"
	@echo "  up               Start the docker containers"
	@echo "  down             Stop the docker containers"
	@echo "  populate         Populate the database with dummy data"
	@echo "  migrate          Apply the migrations"
	@echo "  makemigrations   Generate the migrations"
	@echo "  clean            Stop the docker containers and remove the volumes"
	@echo "  help             Show this help message"

.PHONY: all
all: build

.PHONY: build
build:
	@docker compose -f $(DOCKER_COMPOSE_FILE) build

.PHONY: up
up:
	@docker compose -f $(DOCKER_COMPOSE_FILE) up

.PHONY: down
down:
	@docker compose -f $(DOCKER_COMPOSE_FILE) down

.PHONY: populate
populate:
	@docker compose -f $(DOCKER_COMPOSE_FILE) run $(WEB_SERVICE) python populate_db.py

.PHONY: migrate
migrate:
	@docker compose -f $(DOCKER_COMPOSE_FILE) run $(WEB_SERVICE) flask db upgrade

.PHONY: makemigrations
makemigrations:
	@docker compose -f $(DOCKER_COMPOSE_FILE) run $(WEB_SERVICE) flask db migrate

.PHONY: clean
clean:
	@docker compose -f $(DOCKER_COMPOSE_FILE) down --volumes --remove-orphans
