from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from ..context import get_request_id
from .model import ErrorResponse


class ProdkitExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        try:
            return await call_next(request)
        except Exception as exc:
            payload = ErrorResponse(
                code="internal_error",
                message="Internal server error",
                request_id=get_request_id(),
                details={"exception": type(exc).__name__},
            )
            return JSONResponse(
                status_code=500, content=payload.model_dump(exclude_none=True)
            )


def install_error_handlers(app: FastAPI, *, include_details: bool) -> None:
    @app.exception_handler(HTTPException)
    async def http_exception_handler(_: Request, exc: HTTPException):
        payload = ErrorResponse(
            code="http_error",
            message=str(exc.detail),
            request_id=get_request_id(),
            details={"status_code": exc.status_code} if include_details else None,
        )
        return JSONResponse(
            status_code=exc.status_code, content=payload.model_dump(exclude_none=True)
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exc: RequestValidationError):
        payload = ErrorResponse(
            code="validation_error",
            message="Request validation failed",
            request_id=get_request_id(),
            details={"errors": exc.errors()} if include_details else None,
        )
        return JSONResponse(status_code=422, content=payload.model_dump(exclude_none=True))

