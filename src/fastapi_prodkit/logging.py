from __future__ import annotations

import logging
from typing import Any

import structlog

from .context import get_request_id


def _add_context(logger: Any, method_name: str, event_dict: dict) -> dict:
    rid = get_request_id()
    if rid:
        event_dict["request_id"] = rid
    return event_dict


def configure_logging(*, service_name: str, environment: str, json_logs: bool) -> None:
    logging.basicConfig(level=logging.INFO)

    processors = [
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        _add_context,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    renderer = structlog.processors.JSONRenderer() if json_logs else structlog.dev.ConsoleRenderer()

    structlog.configure(
        processors=processors + [renderer],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        cache_logger_on_first_use=True,
    )

    # bind defaults (service/env) via a global logger factory usage pattern
    structlog.get_logger().bind(service=service_name, env=environment)
