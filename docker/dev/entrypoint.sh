#!/usr/bin/env bash
set -euo pipefail

#check if fastapi_prodkit is installed in the venv
if ! /opt/venv/bin/python -c "import fastapi_prodkit" >/dev/null 2>&1; then
  /opt/venv/bin/pip install -e /workspace
fi

exec /opt/venv/bin/python -m uvicorn examples.app.main:app --host 0.0.0.0 --port 8000 --reload