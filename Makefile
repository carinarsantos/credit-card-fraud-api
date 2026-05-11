# Variáveis
PYTHON = venv/bin/python
PIP = venv/bin/pip
PYTEST = venv/bin/pytest

.PHONY: setup install test run-api run-app docker-up clean help

help:
	@echo "Comandos disponíveis:"
	@echo "  make setup      - Cria o ambiente virtual e instala dependências"
	@echo "  make install    - Instala dependências do requirements.txt"
	@echo "  make test       - Executa a suíte de testes com Pytest"
	@echo "  make run-api    - Inicia o servidor FastAPI (Backend)"
	@echo "  make run-app    - Inicia o dashboard Streamlit (Frontend)"
	@echo "  make docker-up  - Sobe toda a stack via Docker Compose"
	@echo "  make clean      - Remove arquivos temporários e caches"

setup:
	python3 -m venv venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

install:
	$(PIP) install -r requirements.txt

test:
	$(PYTHON) -m pytest tests/

run-api:
	$(PYTHON) -m uvicorn src.api.routes:app --reload

run-app:
	$(PYTHON) -m streamlit run app/dashboard.py

docker-up:
	docker-compose up --build

clean:
	rm -rf venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -f *.sqlite