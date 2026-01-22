.PHONY: run fmt lint test

run:
	python -m uvicorn app.main:app --reload

fmt:
	python -m black .
	python -m ruff check . --fix

lint:
	python -m ruff check .
	python -m mypy app

test:
	python -m pytest
