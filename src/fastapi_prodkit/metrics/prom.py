from __future__ import annotations

from fastapi import FastAPI


def install_prometheus_metrics(app: FastAPI, *, metrics_path: str) -> None:
    try:
        from prometheus_fastapi_instrumentator import Instrumentator
    except Exception as e:  # pragma: no cover
        raise RuntimeError("Install with extras: pip install fastapi-prodkit[metrics]") from e

    Instrumentator().instrument(app).expose(app, endpoint=metrics_path, include_in_schema=False)
