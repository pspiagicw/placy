"""Module to provide simple http test."""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from dotenv import dotenv_values
from backend.database import MongoService
from backend.routes import Router
from backend.logging import DefaultLogger
from faker import Faker

from backend.placy import Placy

app = FastAPI()
# Testing config
config = {
    "SECRET_KEY": "someusefulpassword",
    "MONGO_URI": "mongodb://localhost:27017",
}
database = MongoService()
router = Router(database, config)
logger = DefaultLogger()
placy = Placy(
    app=app,
    databaseService=database,
    loggingService=logger,
    config=config,
    router=router,
)
placy.setup()
placy.routes()
client = TestClient(app)


def test_health():
    """Simple function for testing health of API."""
    response = client.get("/health")
    assert response.status_code == 200, "Status code not 200"
    assert response.json() == {"status": "OK"}


def test_signup():
    """Test user signup functionality."""
    user_payload = generate_user()

    response = client.post("/signup", json=user_payload)
    assert response.status_code == 200, "Status code not 200."
    assert response.json()["isSuccess"], "Request not a success."


def test_login():
    """Test user login functionality."""
    user_payload = generate_user()

    response = client.post("/signup", json=user_payload)
    assert response.status_code == 200, "Status code not 200."
    assert response.json()["isSuccess"], "Request not a success."

    response = client.post("/login", json=user_payload)
    assert response.status_code == 200, "Status code not 200."
    json_response = response.json()
    assert json_response["isSuccess"], "Request not a success."
    assert json_response["token"], "Token empty"


def test_wrong_password():
    """Test user with wrong password."""
    user_payload = generate_user()

    response = client.post("/signup", json=user_payload)
    assert response.status_code == 200, "Status code not 200."
    assert response.json()["isSuccess"], "Request not a success."

    # Make a wrong
    user_payload["password"] = "wrongpassword"

    response = client.post("/login", json=user_payload)
    assert response.status_code == 200, "Status code not 200."
    json_response = response.json()
    assert json_response["isSuccess"], "Request not a success."
    assert json_response["token"], "Token empty"


def generate_user() -> dict[str, str]:
    """Generate a fake user for testing."""
    faker = Faker()
    user_payload = {
        "email": faker.email(),
        "password": faker.password(),
        "username": faker.user_name(),
        "role": "user",
    }

    return user_payload
