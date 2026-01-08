from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastapi_prodkit import ProdkitConfig, setup_app


def test_metrics_disabled_by_default():
    """Tests that the /metrics endpoint is not available by default."""
    app = FastAPI()
    setup_app(app)
    client = TestClient(app)

    response = client.get("/metrics")
    assert response.status_code == 404


def test_metrics_enabled():
    """Tests that the /metrics endpoint is available when enabled."""
    app = FastAPI()
    # Need to add a dummy route to instrument
    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    setup_app(app, ProdkitConfig(enable_metrics=True))
    client = TestClient(app)

    # Make a request to generate metrics
    client.get("/")

    response = client.get("/metrics")
    assert response.status_code == 200
    # Check for some content that should be in a Prometheus scrape
    assert 'http_requests_latency_seconds_bucket' in response.text
    assert 'fastapi_app_info' in response.text
