.PHONY: setup run test lint clean

setup:
	python3.11 -m venv venv
	. venv/bin/activate && pip install --upgrade pip setuptools wheel
	. venv/bin/activate && pip install -r requirements.txt

run:
	. venv/bin/activate && streamlit run app.py

test:
	. venv/bin/activate && pytest tests/ -v

lint:
	. venv/bin/activate && ruff check src/ tests/
	. venv/bin/activate && black --check src/ tests/ app.py

format:
	. venv/bin/activate && black src/ tests/ app.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf data/cache/*.db data/vectordb/*
