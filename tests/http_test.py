"""Module to provide simple http test."""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.placy import Placy

app = FastAPI()

placy = Placy(app, None, {})
placy.setup_routes()
client = TestClient(app)


def test_health():
    """Simple function for testing health of API."""
    response = client.get("/health")
    assert response.status_code == 200, "Status code not 200"
    assert response.json() == {"status": "OK"}
