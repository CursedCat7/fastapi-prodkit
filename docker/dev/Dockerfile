FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
      bash curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv && /opt/venv/bin/pip install --upgrade pip

WORKDIR /workspace

# dev install in venv
COPY pyproject.toml README.md /workspace/
ARG PIP_EXTRAS="dev,metrics,tracing"
RUN /opt/venv/bin/pip install ".[${PIP_EXTRAS}]"

COPY docker/dev/entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]