# AI Job Application Assistant - Development Commands

.PHONY: help install dev test clean docker-up docker-down

help:  ## Show this help message
	@echo "AI Job Application Assistant - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install Python dependencies
	pip install -r requirements.txt

dev:  ## Start development server
	python run.py

test:  ## Run tests
	pytest tests/ -v

test-coverage:  ## Run tests with coverage
	pytest tests/ --cov=src --cov-report=html

lint:  ## Run code linting
	flake8 src/ tests/
	black --check src/ tests/

format:  ## Format code
	black src/ tests/

docker-up:  ## Start Docker services
	docker-compose up -d

docker-down:  ## Stop Docker services
	docker-compose down

docker-logs:  ## View Docker logs
	docker-compose logs -f

clean:  ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .coverage htmlcov/

setup:  ## Complete setup (install + docker + test)
	@if [ ! -f .env ]; then \
		echo "Creating .env file from .env.example..."; \
		cp .env.example .env; \
		echo "Please edit .env file with your configuration"; \
	fi
	make install
	make docker-up
	sleep 10
	make test

check-deps:  ## Check if all dependencies are available
	@echo "Checking Python version..."
	@python --version
	@echo "Checking Docker..."
	@docker --version
	@echo "Checking Docker Compose..."
	@docker-compose --version
	@echo "All dependencies are available!"

db-reset:  ## Reset all databases (WARNING: This will delete all data)
	docker-compose down -v
	docker-compose up -d
	sleep 10
	@echo "Databases reset successfully!"