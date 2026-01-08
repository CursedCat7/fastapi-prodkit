from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel

from fastapi_prodkit import ProdkitConfig, setup_app


def test_http_exception_handler():
    """Tests that a standard HTTPException is formatted correctly."""
    app = FastAPI()
    setup_app(app)

    @app.get("/http-error")
    def raise_http_error():
        raise HTTPException(status_code=418, detail="I'm a teapot")

    client = TestClient(app)
    response = client.get("/http-error")

    assert response.status_code == 418
    body = response.json()
    assert body["code"] == "http_error"
    assert body["message"] == "I'm a teapot"
    assert "request_id" in body


def test_validation_error_handler():
    """Tests that a Pydantic validation error is formatted correctly."""
    app = FastAPI()
    setup_app(app)

    class Item(BaseModel):
        name: str
        price: float

    @app.post("/items/")
    def create_item(item: Item):
        return item

    client = TestClient(app)
    # Send incorrect data type for 'price'
    response = client.post("/items/", json={"name": "Screwdriver", "price": "invalid"})

    assert response.status_code == 422
    body = response.json()
    assert body["code"] == "validation_error"
    assert body["message"] == "Request validation failed"
    assert "request_id" in body
