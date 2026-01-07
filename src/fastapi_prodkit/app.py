from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from fastapi import FastAPI

from .errors.handlers import install_error_handlers
from .health.router import install_health_routes
from .logging import configure_logging
from .middleware.request_context import RequestContextMiddleware


@dataclass(frozen=True)
class ProdkitConfig:
    service_name: str = "app"
    environment: str = "dev"  # dev/stage/prod

    request_id_header: str = "X-Request-ID"
    generate_request_id: bool = True
    expose_request_id_header: bool = True

    json_logs: bool = True
    access_log: bool = False  # MVP default to False, enable when needed

    include_error_details_in_response: bool = False

    health_path: str = "/healthz"
    ready_path: str = "/readyz"

    enable_metrics: bool = False
    metrics_path: str = "/metrics"

    enable_tracing: bool = False

    # readiness check hook (optional)
    readiness_check: Callable[[], bool] | None = None


def setup_app(app: FastAPI, config: ProdkitConfig | None = None) -> FastAPI:
    cfg = config or ProdkitConfig()

    configure_logging(
        service_name=cfg.service_name, environment=cfg.environment, json_logs=cfg.json_logs
    )

    # Request context middleware (request_id + contextvars)
    app.add_middleware(
        RequestContextMiddleware,
        request_id_header=cfg.request_id_header,
        generate_request_id=cfg.generate_request_id,
        expose_request_id_header=cfg.expose_request_id_header,
    )

    install_error_handlers(app, include_details=cfg.include_error_details_in_response)
    install_health_routes(
        app,
        health_path=cfg.health_path,
        ready_path=cfg.ready_path,
        readiness_check=cfg.readiness_check,
    )

    if cfg.enable_metrics:
        from .metrics.prom import install_prometheus_metrics  # lazy import

        install_prometheus_metrics(app, metrics_path=cfg.metrics_path)

    if cfg.enable_tracing:
        from .tracing.otel import install_otel  # lazy import

        install_otel(app, service_name=cfg.service_name)

    return app
