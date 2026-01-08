from __future__ import annotations

from collections.abc import Callable

from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse


def install_health_routes(
    app: FastAPI,
    *,
    health_path: str,
    ready_path: str,
    readiness_check: Callable[[], bool] | None = None,
) -> None:
    router = APIRouter()

    @router.get(health_path, tags=["health"])
    def healthz():
        return {"status": "ok"}

    @router.get(ready_path, tags=["health"])
    def readyz():
        if readiness_check is None or readiness_check():
            return {"status": "ok"}
        return JSONResponse(status_code=503, content={"status": "unavailable"})

    app.include_router(router)
