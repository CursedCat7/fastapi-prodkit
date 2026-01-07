FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
      bash curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv && pip install --upgrade pip

WORKDIR /workspace


COPY pyproject.toml README.md /workspace/


ARG PIP_EXTRAS="dev,metrics,tracing"
RUN pip install -e ".[${PIP_EXTRAS}]"


CMD ["bash", "-lc", "uvicorn examples.app.main:app --host 0.0.0.0 --port 8000 --reload"]