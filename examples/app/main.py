#for example test
from fastapi import FastAPI
from fastapi_prodkit import ProdkitConfig, setup_app

app = FastAPI(title="prodkit-example")

setup_app(
    app,
    ProdkitConfig(
        service_name="prodkit-example",
        environment="dev",
        enable_metrics=True,
        enable_tracing=False,
        include_error_details_in_response=True,
    ),
)

@app.get("/ping")
def ping():
    return {"ok": True}

@app.get("/boom")
def boom():
    raise RuntimeError("crash")