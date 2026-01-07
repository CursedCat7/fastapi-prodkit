from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from ..context import get_request_id
from .model import ErrorResponse


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

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_: Request, exc: Exception):
        payload = ErrorResponse(
            code="internal_error",
            message="Internal server error",
            request_id=get_request_id(),
            details={"exception": type(exc).__name__} if include_details else None,
        )
        return JSONResponse(status_code=500, content=payload.model_dump(exclude_none=True))
