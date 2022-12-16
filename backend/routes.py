"""Module to route all backend requests."""
from fastapi import FastAPI

from backend.models import Health


app = FastAPI()


@app.get("/health")
def checkhealth():
    """Route to handle health request."""
    return {"Status": "OK"}
