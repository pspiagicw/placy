"""Module to provide simple http test."""


from fastapi.testclient import TestClient

from authentication.routes import app

client = TestClient(app)


def test_health():
    """Simple function for testing health of API."""
    response = client.get("/health")
    assert response.status_code == 200, "Status code not 200"
    assert response.json() == {"status": "OK"}


def test_echo():
    """Simple function for testing echo of JSON."""
    response = client.post("/echo", json={"version": "1.0", "client": "mobile"})

    assert response.status_code == 200
    assert response.json() == {"version": "1.0", "client": "mobile"}
