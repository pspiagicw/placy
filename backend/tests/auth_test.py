"""Module to provide simple http test."""

from dotenv import dotenv_values
from faker import Faker
from fastapi import FastAPI
from fastapi.testclient import TestClient
from placy.controllers.auth import AuthController
from placy.services.database import MongoService
from placy.services.logging import DefaultLogger

from placy.placy import Placy

app = FastAPI()
# Testing config
config = {
    "SECRET_KEY": "someusefulpassword",
    "MONGO_URI": "mongodb://localhost:27017",
}
database = MongoService()
authController = AuthController(database, config)
logger = DefaultLogger()
placy = Placy(
    app=app,
    databaseService=database,
    loggingService=logger,
    config=config,
    authController=authController,
)
placy.setup()
placy.routes()
client = TestClient(app)


def assertSignUp(user: dict[str, str]):
    """Assert signup is working and possible."""
    response = client.post("/auth/signup", json=user)
    assert response.status_code == 200, "Status code not 200."
    assert response.json()["success"], "Request not a success."


def assertLogin(user: dict[str, str]) -> str:
    """Assert login is working and possible."""
    response = client.post("/auth/login", json=user)
    assert response.status_code == 200, "Status code not 200."

    json_response = response.json()

    assert json_response["success"], "Request not a success."
    assert json_response["token"], "Token empty"
    assert json_response["refresh"], "Refresh Token empty."
    return json_response["token"]


def test_health():
    """Simple function for testing health of API."""
    response = client.get("/health")
    assert response.status_code == 200, "Status code not 200"
    assert response.json() == {"status": "OK", "version": 0.1}


def test_signup():
    """Test user signup functionality."""
    user = generate_user()
    assertSignUp(user)


def test_login():
    """Test user login functionality."""
    user = generate_user()
    assertSignUp(user)
    assertLogin(user)


def test_wrong_password():
    """Test user with wrong password."""
    user = generate_user()
    assertSignUp(user)
    assertLogin(user)

    # Make a wrong password
    user["password"] = "wrongpassword"

    response = client.post("/auth/login", json=user)
    assert response.status_code == 400, "Status code not 400."
    json_response = response.json()
    assert not json_response["success"], json_response["errmsg"]
    assert "token" not in json_response, "Token present"


def test_token_refresh():
    """Test token refresh endpoint."""
    user = generate_user()

    assertSignUp(user)

    token = assertLogin(user)

    response = client.get(
        "/auth/refresh",
        headers={"Authorization": f"Bearer {token}"},
    )

    json_response = response.json()

    assert json_response["success"], json_response["errmsg"]
    assert response.status_code == 200, "Response not a success"
    assert json_response["token"], "Token empty"
    assert json_response["refresh"], "Refresh token empty"


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
