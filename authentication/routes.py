"""Module to route all authentication requests."""
from fastapi import FastAPI

from authentication.models import Health


app = FastAPI()


@app.get("/health")
def checkhealth():
    """Route to handle health request."""
    return {"Status": "OK"}
