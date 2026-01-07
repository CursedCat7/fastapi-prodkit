from __future__ import annotations

from fastapi import FastAPI


def install_otel(app: FastAPI, *, service_name: str) -> None:
    try:
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    except Exception as e:  # pragma: no cover
        raise RuntimeError("Install with extras: pip install fastapi-prodkit[tracing]") from e

    # only instrumentation(Exporter/SDK should be configured in env))
    FastAPIInstrumentor.instrument_app(app)