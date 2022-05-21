.PHONY: init \
init-venv \
create-venv \
update-venv \
clean \ \
clean-venv \
clean-pyc \
clean-test \
test \
coverage \
print \
postgres-down \
postgres-up \
service-run \
up \
down \

.DEFAULT_GOAL := help

# Tests
TARGET ?= tests
REMOTE_DOMAIN = ""


############################################################################
## Target definitions
## This section will define the projects make targets
############################################################################

help:
	@echo "    init"
	@echo "        Initialize development environment."
	@echo "    init-venv"
	@echo "        Initialize Python environment."
	@echo "    create-venv"
	@echo "        Creates Python environment."
	@echo "    clean"
	@echo "        Remove all the development environment files."
	@echo "    clean-venv"
	@echo "        Remove Python virtual environment."
	@echo "    clean-pyc"
	@echo "        Remove Python artifacts."
	@echo "    clean-test"
	@echo "        Remove test artifacts."
	@echo "    test"
	@echo "        Run pytest. Must prefix with POSTGRES_PORT=12733"
	@echo "    coverage"
	@echo "        Generate coverage report."
	@echo "    print"
	@echo "        Show the complete yaml of a particular deploy."
	@echo "    postgres-up"
	@echo "        Start a local postgres."
	@echo "    postgres-down"
	@echo "        Stop a local postgres."
	@echo "    up"
	@echo "        Start infrastructure and run service."
	@echo "    down"
	@echo "        Build and publish client library."
	@echo "    service-up"
	@echo "        Start the service container."



# -----------------------------
# Environment Setup
# Python Init & Clean
# -----------------------------
 ifeq (, $(shell which poetry))
 $(error "Poetry is required to run this project. No Poetry in $(PATH), consider installing from https://python-poetry.org/en/latest/")
 endif

init: clean init-venv pre-commit-install

init-venv: clean-venv create-venv
	@echo ""
	@echo "Initializing Poetry environment"
	@poetry update

create-venv:
	@echo "Creating virtual environment..."
	@poetry env use 3.9.9

update-venv:
	@echo ""
	@echo "Updating Poetry environment"
	@poetry update

pre-commit-install:
	@( \
		. `poetry env info --path`/bin/activate; \
		pre-commit install; \
	)

clean: clean-pyc clean-test clean-venv


clean-venv:
	@echo "Removing Poetry virtual environment: $(VENV)..."
	@rm -rf `poetry env info --path`

clean-pyc:
	@echo "Removing compiled bytecode files..."
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +


clean-test: clean-pyc
	@echo "Removing previous test data..."
	@rm -rf .coverage
	@rm -rf htmlcov
	@rm -rf test-reports
	@rm -f coverage.xml
	@rm -rf .pytest_cache


# -----------------------------
# Testing
# Executing and orchestrating the test suites
# -----------------------------

test: clean-test test-pytest

test-pytest:
	@echo "Running pytest..."
	@( \
		. `poetry env info --path`/bin/activate; \
		pytest; \
	)

coverage: clean-test coverage-pytest

coverage-pytest:
	@echo "Running test with coverage report..."
	@( \
		. `poetry env info --path`/bin/activate; \
		POSTGRES_PORT=$(POSTGRES_PORT) pytest $(TARGET)\
			--cov=src \
			--cov-report html \
			--cov-report term-missing:skip-covered \
			--junitxml=test-reports/junit.xml \
            --no-cov-on-fail; \
	)

# -----------------------------
# Local Execution
# This section contains all the needed targets
# for the local run of the service in the
# developer environment
# -----------------------------

down:
	@docker-compose rm --stop --force app

up: postgres-up service-up

service-up:
	@docker-compose up -d service

service-down:
	@docker-compose up -d service

postgres-up:
	@echo "Starting postgres..."
	@docker-compose up -d db
	@sleep 5

postgres-down:
	@echo "Stopping postgres..."
	@docker-compose rm --stop --force db


