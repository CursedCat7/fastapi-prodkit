# fastapi-prodkit

**Modular production rails for FastAPI.**  
Install request context (request-id), structured logging, standard error responses, health endpoints, and optional metrics/tracing — with a small, explicit API.

> Goal: make “production basics” the default, without forcing an application template or a specific infra stack.

---

## What this project does

`fastapi-prodkit` is a library you add to an existing FastAPI app:

- **Request context**
  - Reads an incoming request id header (default: `X-Request-ID`)
  - Generates a request id if missing
  - Optionally echoes the request id back in the response header
  - Propagates the request id through the request lifecycle via `contextvars`
- **Logging**
  - Structured logs (JSON by default; console-friendly option available)
  - Automatic injection of request context into logs (e.g., `request_id`)
- **Errors**
  - Standard error response schema for:
    - `HTTPException`
    - Request validation errors
    - Unhandled exceptions (500)
  - Production-safe defaults (no internal stack traces in responses)
- **Health endpoints**
  - Liveness: `/healthz`
  - Readiness: `/readyz` (optional hook for your dependency checks)
- **Optional observability**
  - **Prometheus** `/metrics` (extra: `metrics`)
  - **OpenTelemetry** instrumentation (extra: `tracing`)

---

## Non-goals

`fastapi-prodkit` is **not**:

- A project template / cookiecutter
- An ORM, migration, auth, rate-limit, or caching framework
- A vendor lock-in for a single monitoring stack

---

> **Note**: `fastapi-prodkit` is not published on PyPI yet.  
> For now, install from GitHub (or from a local checkout). PyPI distribution will be added later.

### Install (GitHub)

    python -m pip install "git+https://github.com/CursedCat7/fastapi-prodkit.git"

### Install (local, editable)

    git clone https://github.com/CursedCat7/fastapi-prodkit.git
    cd fastapi-prodkit
    python -m pip install -e .

Optional extras:

    python -m pip install -e ".[dev,metrics,tracing]"

---

## Install (PyPI) - coming later

    pip install fastapi-prodkit

Optional extras:

    pip install "fastapi-prodkit[metrics]"
    pip install "fastapi-prodkit[tracing]"
    pip install "fastapi-prodkit[dev]"   # contributors

---



## Quickstart

    from fastapi import FastAPI
    from fastapi_prodkit import setup_app, ProdkitConfig

    app = FastAPI(title="my-service")

    setup_app(
        app,
        ProdkitConfig(
            service_name="my-service",
            environment="dev",
            enable_metrics=True,
            enable_tracing=False,
            include_error_details_in_response=False,
        ),
    )

    @app.get("/ping")
    def ping():
        return {"ok": True}

Run:

    uvicorn examples.app.main:app --reload --port 8000

---

## What you get (behavior)

### Request ID

- If the client provides `X-Request-ID`, it will be used.
- Otherwise, a UUID is generated (if enabled).
- The server can echo the request id back.

Example response header:

    X-Request-ID: 9f6b1b0f-2a59-4d6f-bb40-9a7d9e1d2e7a

### Standard error schema

Errors are returned in a consistent JSON shape:

    {
      "code": "internal_error",
      "message": "Internal server error",
      "request_id": "9f6b1b0f-2a59-4d6f-bb40-9a7d9e1d2e7a"
    }

Validation errors:

    {
      "code": "validation_error",
      "message": "Request validation failed",
      "request_id": "..."
    }

### Health endpoints

- `GET /healthz` → `200 {"status":"ok"}`
- `GET /readyz` → `200 {"status":"ok"}`
  - Optionally returns not-ready if your hook fails.

---

## Configuration

`ProdkitConfig` is the primary configuration surface.

Key options:

- `service_name`, `environment`
- `request_id_header`, `generate_request_id`, `expose_request_id_header`
- `json_logs`
- `include_error_details_in_response`
- `health_path`, `ready_path`
- `enable_metrics`, `metrics_path`
- `enable_tracing`
- `readiness_check` (callable)

Example readiness hook:

    def readiness_check() -> bool:
        # check DB/redis connectivity etc.
        return True

    setup_app(app, ProdkitConfig(readiness_check=readiness_check))

---

## Metrics (Prometheus)

Install and enable:

    pip install "fastapi-prodkit[metrics]"

    setup_app(app, ProdkitConfig(enable_metrics=True, metrics_path="/metrics"))

Then `GET /metrics` is exposed (not included in OpenAPI schema by default).

---

## Tracing (OpenTelemetry)

Install and enable:

    pip install "fastapi-prodkit[tracing]"

    setup_app(app, ProdkitConfig(enable_tracing=True))

This enables FastAPI instrumentation. Exporter/SDK configuration is typically done via environment variables or your application’s OTel setup.

---

## Docker Compose development environment

This repository includes a compose-based dev environment with optional profiles:

- `core`: API only
- `metrics`: Prometheus + Grafana
- `tracing`: OTel Collector + Jaeger

Examples:

    docker compose --profile core up -d --build
    docker compose --profile core --profile metrics up -d --build
    docker compose --profile core --profile tracing up -d --build
    docker compose --profile core --profile metrics --profile tracing up -d --build

Default endpoints:

- API: `http://localhost:8000`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000` (admin/admin)
- Jaeger: `http://localhost:16686`

---

## Compatibility

- Python: 3.11+
- FastAPI: modern stable versions (the library aims to track current FastAPI/Starlette)

---

## Development

Install dev dependencies:

    pip install -e ".[dev]"

Run tests:

    pytest

Lint:

    ruff check .

---

## Contributing

Contributions are welcome, especially:

- Middleware correctness & edge cases
- Version compatibility testing
- Documentation and examples

See [CONTRIBUTING.md](CONTRIBUTING.md) for workflow and expectations.

---

## Security

This is a personal side project maintained on a best-effort basis.  
Please report vulnerabilities via the process described in [SECURITY.md](SECURITY.md).

---

## License

MIT. See [LICENSE](LICENSE).

---

## Roadmap (early-stage)

- Stabilize public API (`setup_app`, `ProdkitConfig`)
- Improve readiness hook behavior (async support, richer status output)
- Optional access logs as structured events (avoid duplicate logging)
- More explicit error code taxonomy / RFC7807 alignment (evaluate)
- Documentation and examples for:
  - Reverse proxy request-id propagation
  - Securing `/metrics` in production
  - OTel exporter setup patterns

---

## Philosophy

- **Modular**: adopt incrementally
- **Opinionated defaults**: safe-by-default for production
- **Minimal surface area**: small public API, predictable behavior
- **Composable**: does not block your architecture or infra choices
