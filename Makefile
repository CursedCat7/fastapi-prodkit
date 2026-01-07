.PHONY: dev test lint compose compose-metrics compose-tracing

dev:
	uvicorn examples.app.main:app --reload --port 8000

test:
	pytest -q

lint:
	ruff check .

compose:
	docker compose --profile core up --build

compose-metrics:
	docker compose --profile core --profile metrics up --build

compose-tracing:
	docker compose --profile core --profile tracing up --build