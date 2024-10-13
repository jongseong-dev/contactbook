DJANGO_WORKDIR = backend
DJANGO_SETTINGS_MODULE = config.settings.local
DJANGO_SECRET_KEY = local
CELERY_APP_NAME = config

.PHONY:  virtualenv create-env install infra celery migration test clean

virtualenv:
	@echo "Virtualenv with poetry and pyenv. Python version: 3.11.8"
	pyenv local 3.11.8
	poetry env use 3.11.8
	poetry shell

setting: create-env install infra celery migration
	@echo "Setting up dependencies required for development "

create-env:
	@echo "Create env file"
	@echo "If env file exists, skipping this process.."
	@if [ -f $(DJANGO_WORKDIR)/.env ]; then \
		echo "Env File already exists."; \
	else \
		echo "DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS_MODULE)" > $(DJANGO_WORKDIR)/.env; \
		echo "DJANGO_SECRET_KEY=$(DJANGO_SECRET_KEY)" >> $(DJANGO_WORKDIR)/.env; \
		cat $(DJANGO_WORKDIR)/.env; \
	fi

install:
	@echo "Installing dependencies..."
	poetry install --no-root

infra:
	@echo "Run infrastructure containers needed for the development environment."
	docker-compose -f infra/docker-compose.yml up --build -d

migration:
	@echo "Migration..."
	cd ${DJANGO_WORKDIR} && \
	python manage.py migrate

test: infra celery-worker
	@echo "Running tests..."
	cd ${DJANGO_WORKDIR} && \
	pytest

clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -type f -path "*/migrations/*.pyc" -delete