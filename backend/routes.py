"""Module to route all backend requests."""

from backend.database import DatabaseService
from backend.models import User
from typing import Any, Tuple
import http
import jwt
from datetime import datetime, timedelta


class Router:
    """Router handles all routing."""

    def __init__(self, db: DatabaseService, config: dict[str, str]):
        """Construct the Router class."""
        self.db = db
        self.config = config

    def checkhealth(self):
        """Route to handle health request."""
        return {"status": "OK"}

    def signup(self, user: User) -> dict[str, Any]:
        """Route to handle user signup."""
        (id, errmsg, status_code) = self.db.add_user(user)

        if id == "":
            return {
                "status": status_code,
                "isSuccess": False,
                "error": errmsg,
            }

        user_json = user.dict(exclude={"password"}, exclude_none=True)
        user_json["_id"] = str(id)

        return {
            "status": 400,
            "isSuccess": True,
            "error": None,
            "payload": user_json,
        }

    def login(self, user: User):
        """Route to handle user signin."""
        result = self.db.search_user(user)

        if result == None:
            return {
                "status": http.HTTPStatus.NOT_FOUND,
                "isSuccess": False,
                "error": "User not found",
            }

        if result["password"] != user.password:
            return {
                "status": http.HTTPStatus.BAD_REQUEST,
                "isSuccess": False,
                "error": "email/password wrong.",
            }

        (token, refresh) = self.generateToken(user)

        return {
            "status": http.HTTPStatus.OK,
            "isSuccess": True,
            "error": None,
            "payload": user.dict(),
            "token": token,
            "refresh": refresh,
        }

    def generateToken(self, user: User) -> Tuple[str, str]:
        """Generate a pair of JWT Token."""
        payload = user.dict(exclude={"password"}, exclude_none=True)

        payload["exp"] = datetime.now() + timedelta(days=1)

        key = ""
        if "SECRET_KEY" in self.config:
            key = self.config["SECRET_KEY"]
        else:
            return ("", "")

        token = jwt.encode(payload=payload, key=key)

        payload["exp"] = datetime.now() + timedelta(days=7)

        refresh = jwt.encode(payload=payload, key=key)

        return (token, refresh)
