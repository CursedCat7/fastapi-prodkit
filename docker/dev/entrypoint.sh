#!/usr/bin/env bash
set -euo pipefail

# venv pip to install editable
/opt/venv/bin/pip install -e /workspace

# venv python
exec /opt/venv/bin/python -m uvicorn examples.app.main:app --host 0.0.0.0 --port 8000 --reload