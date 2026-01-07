from __future__ import annotations

import uuid
from collections.abc import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from ..context import request_id_var


class RequestContextMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        *,
        request_id_header: str,
        generate_request_id: bool,
        expose_request_id_header: bool,
    ) -> None:
        super().__init__(app)
        self._header = request_id_header
        self._generate = generate_request_id
        self._expose = expose_request_id_header

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Response]
    ) -> Response:
        incoming = request.headers.get(self._header)
        rid = incoming or (str(uuid.uuid4()) if self._generate else None)

        token = None
        if rid:
            token = request_id_var.set(rid)

        try:
            response = await call_next(request)
        finally:
            if token is not None:
                request_id_var.reset(token)

        if rid and self._expose:
            response.headers[self._header] = rid
        return response
