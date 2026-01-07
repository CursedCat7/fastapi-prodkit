from __future__ import annotations

from collections.abc import Callable

from fastapi import APIRouter, FastAPI


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
    def readyz():  # for development boot. should be Response(...)
        if readiness_check is None:
            return {"status": "ok"}
        return {"status": "ok"} if readiness_check() else ({"status": "not_ready"}, 503)

    app.include_router(router)
