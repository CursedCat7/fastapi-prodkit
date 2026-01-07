from __future__ import annotations

from typing import Callable, Optional

from fastapi import APIRouter, FastAPI


def install_health_routes(
    app: FastAPI,
    *,
    health_path: str,
    ready_path: str,
    readiness_check: Optional[Callable[[], bool]] = None,
) -> None:
    router = APIRouter()

    @router.get(health_path, tags=["health"])
    def healthz():
        return {"status": "ok"}

    @router.get(ready_path, tags=["health"])
    def readyz(): # for development boot. should be Response(...)
        if readiness_check is None:
            return {"status": "ok"}
        return {"status": "ok"} if readiness_check() else ({"status": "not_ready"}, 503)

    app.include_router(router)