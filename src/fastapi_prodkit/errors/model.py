from __future__ import annotations

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    code: str
    message: str
    request_id: str | None = None
    details: dict | None = None