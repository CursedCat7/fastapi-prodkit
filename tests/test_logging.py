import logging
import io
import json
from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastapi_prodkit import ProdkitConfig, setup_app


def test_json_logging_does_not_crash():
    """
    A simple test to ensure that enabling JSON logging and making a request
    does not cause the application to crash. A more thorough test would
    involve capturing and parsing log output, but this is a good start.
    """
    app = FastAPI()
    setup_app(app, ProdkitConfig(json_logs=True))

    @app.get("/log-test")
    def log_test():
        logging.info("This is a test log message.")
        return {"status": "logged"}

    client = TestClient(app)
    response = client.get("/log-test")

    assert response.status_code == 200
    assert response.json() == {"status": "logged"}
