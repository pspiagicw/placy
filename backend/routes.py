"""Module to route all backend requests."""

from backend.database import DatabaseService
from backend.models import User
from typing import Any
import http


class Router:
    """Router handles all routing."""

    def __init__(self, db: DatabaseService, config: dict[str, str | None]):
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

    def signin(self, user: User):
        """Route to handle user signin."""
        result = self.db.search_user(user)

        if result == None:
            return {
                "status": http.HTTPStatus.NOT_FOUND,
                "isSuccess": False,
                "error": "User not found",
            }

        return {
            "isSuccess": True,
            "error": None,
            "payload": user,
            "token": "Not possible",
            "refresh": "Really not possible",
        }
