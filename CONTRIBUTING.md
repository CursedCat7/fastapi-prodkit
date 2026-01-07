# Contributing

Thanks for considering a contribution to **fastapi-prodkit**.

This is a personal, non-commercial side project maintained on a best-effort basis. I may be slow to respond, but I do review contributions as time allows.

---

## Ways to contribute

- Report bugs (with reproducible steps)
- Improve documentation (README, examples)
- Add tests / fix regressions
- Improve compatibility across FastAPI/Starlette versions
- Propose small, well-scoped features aligned with the project goals

---

## Before you start

### 1) Check existing issues / discussions
If you plan a non-trivial change, please open an issue first to discuss scope and approach.

### 2) Keep changes small
Smaller PRs get reviewed and merged faster:
- One change per PR
- Clear title + description
- Include tests when behavior changes

---

## Development setup

### Local (recommended)

Install dev dependencies:

    python -m pip install -U pip
    python -m pip install -e ".[dev]"

Run lint & formatting:

    python -m ruff check .
    python -m ruff format --check .

Auto-fix lint/format:

    python -m ruff check --fix .
    python -m ruff format .

Run tests:

    python -m pytest -q

### Docker (optional)

If you use the compose dev environment:

    docker compose --profile core up -d --build
    docker compose exec api /opt/venv/bin/python -m pytest -q

---

## Code style

- Formatting: `ruff format`
- Linting: `ruff check`
- Prefer Python 3.11+ idioms (e.g. `X | None`, `collections.abc.Callable`)
- Keep the public API small and explicit (`setup_app`, `ProdkitConfig`)

---

## Tests

- Add tests for behavior changes.
- Prefer fast, isolated tests.
- If you add middleware/handlers, include at least one test covering the happy-path and one covering an error/edge case.

---

## Security issues

Please do not open public issues for vulnerabilities.  
Follow `SECURITY.md` for responsible disclosure.

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License (see `LICENSE`).