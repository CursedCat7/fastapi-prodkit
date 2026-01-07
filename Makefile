.PHONY: dev test lint format-check type-check compose compose-metrics compose-tracing

dev:
	uvicorn examples.app.main:app --reload --port 8000

test:
	pytest -q

lint:
	ruff check .

format-check:
	ruff format . --check

type-check:
	mypy src tests examples

compose:
	docker compose --profile core up --build

compose-metrics:
	docker compose --profile core --profile metrics up --build

compose-tracing:
	docker compose --profile core --profile tracing up --build