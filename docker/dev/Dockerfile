FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates bash \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
COPY pyproject.toml README.md /workspace/

RUN pip install --upgrade pip && pip install -e ".[dev]"

CMD ["bash", "-lc", "uvicorn examples.app.main:app --host 0.0.0.0 --port 8000 --reload"]