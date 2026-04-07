.PHONY: help install lint format test dev adk pre-commit-install clean

help:
	@echo "Comandos disponibles:"
	@echo "  make install            - Instalar dependencias"
	@echo "  make lint               - Verificar código con ruff"
	@echo "  make format             - Formatear código con ruff"
	@echo "  make test               - Ejecutar tests con pytest"
	@echo "  make test-cov           - Ejecutar tests con cobertura"
	@echo "  make dev                - Ejecutar aplicación en development"
	@echo "  make adk                - Lanzar ADK Web UI en puerto 8765"
	@echo "  make pre-commit-install - Instalar pre-commit hooks"
	@echo "  make clean              - Limpiar archivos temporales"

install:
	pip install -r requirements.txt

lint:
	ruff check app/

format:
	ruff format app/
	ruff check app/ --fix

test:
	pytest app/tests/ -v

test-cov:
	pytest app/tests/ --cov=app --cov-report=html --cov-report=term

dev:
	fastapi dev app/main.py

adk:
	PYTHONPATH=. adk web app --port 8765

pre-commit-install:
	pip install pre-commit
	cd .. && pre-commit install --config backend/.pre-commit-config.yaml