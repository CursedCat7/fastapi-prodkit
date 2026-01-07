#for test
from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastapi_prodkit import ProdkitConfig, setup_app


def test_request_id_header_is_set():
    app = FastAPI()
    setup_app(app, ProdkitConfig(expose_request_id_header=True))
    app.get("/ping")(lambda: {"ok": True})

    client = TestClient(app)
    r = client.get("/ping")
    assert "X-Request-ID" in r.headers
    assert r.headers["X-Request-ID"]

def test_standard_error_schema():
    app = FastAPI()
    setup_app(app, ProdkitConfig(include_error_details_in_response=False))
    app.get("/boom")(lambda: 1 / 0)

    client = TestClient(app)
    r = client.get("/boom")
    assert r.status_code == 500
    body = r.json()
    assert body["code"] == "internal_error"
    assert "request_id" in body