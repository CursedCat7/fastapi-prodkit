#!/bin/bash
set -e
function usage() {
  echo "Usage: $0 {dev|test|lint|format-check|type-check|compose|compose-metrics|compose-tracing|all}"
  echo "  dev: Run the development server locally"
  echo "  test: Run pytest tests"
  echo "  lint: Run ruff linter"
  echo "  format-check: Check code formatting with ruff"
  echo "  type-check: Run mypy type checker"
  echo "  compose: Run docker-compose with core profile"
  echo "  compose-metrics: Run docker-compose with metrics profile"
  echo "  compose-tracing: Run docker-compose with tracing profile"
  echo "  all: Run lint, format-check, test, and type-check"
  exit 1
}
if [ $# -eq 0 ]; then
  usage
fi
case "$1" in
  dev)
    echo "Running development server..."
    make dev
    ;;
  test)
    echo "Running tests..."
    make test
    ;;
  lint)
    echo "Running linter..."
    make lint
    ;;
  format-check)
    echo "Checking code formatting..."
    make format-check
    ;;
  type-check)
    echo "Running type checker..."
    make type-check
    ;;
  compose)
    echo "Running docker-compose with core profile..."
    make compose
    ;;
  compose-metrics)
    echo "Running docker-compose with metrics profile..."
    make compose-metrics
    ;;
  compose-tracing)
    echo "Running docker-compose with tracing profile..."
    make compose-tracing
    ;;
  all)
    echo "Running lint, format-check, test, and type-check..."
    make lint
    make format-check
    make test
    make type-check
    echo "All checks passed!"
    ;;
  *)
    usage
    ;;
esac
exit 0