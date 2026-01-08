from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastapi_prodkit import ProdkitConfig, setup_app


def test_healthz_endpoint():
    """Tests that the /healthz endpoint is available and returns a 200."""
    app = FastAPI()
    setup_app(app)
    client = TestClient(app)

    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readyz_endpoint_default():
    """Tests that the /readyz endpoint is available and returns 200 by default."""
    app = FastAPI()
    setup_app(app)
    client = TestClient(app)

    response = client.get("/readyz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readyz_with_successful_check():
    """Tests /readyz with a readiness_check hook that returns True."""
    app = FastAPI()
    setup_app(app, ProdkitConfig(readiness_check=lambda: True))
    client = TestClient(app)

    response = client.get("/readyz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readyz_with_failing_check():
    """Tests /readyz with a readiness_check hook that returns False."""
    app = FastAPI()
    setup_app(app, ProdkitConfig(readiness_check=lambda: False))
    client = TestClient(app)

    response = client.get("/readyz")
    assert response.status_code == 503
    assert response.json()["status"] == "unavailable"
