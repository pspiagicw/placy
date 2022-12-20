"""Module to route all backend requests."""

from placy.database import DatabaseService
from placy.models import OTP, Email, User, UpdatePassword
from typing import Any, Tuple
import http
import random
import jwt
from datetime import datetime, timedelta


class Router:
    """Router handles all routing."""

    def __init__(self, db: DatabaseService, config: dict[str, str]):
        """Construct the Router class."""
        self.db = db
        self.config = config

    def generate_otp(self, email: str) -> OTP:
        """Generate a OTP instance."""
        otp = "".join([str(random.randint(0, 9)) for _ in range(6)])

        exp = datetime.now() + timedelta(minutes=15)

        instance = OTP(email=email, otp=otp, exp=exp, used=False)
        return instance

    def reset(self, update: UpdatePassword) -> Tuple[dict[str, Any], int]:
        """Route to handle reset password requests."""
        return ({"isSuccess": False, "error": "Not implemented yet."}, 500)

    def forgot(self, email: Email) -> Tuple[dict[str, Any], int]:
        """Route to handle forgot password requests."""
        otp = self.generate_otp(email.email)

        (id, errmsg, status_code) = self.db.add_otp(otp)

        if id == "":
            return (
                {
                    "isSuccess": False,
                    "error": errmsg,
                },
                status_code,
            )

        return (
            {
                "isSuccess": True,
                "error": None,
            },
            200,
        )

    def refresh(self, token_header: str | None) -> Tuple[dict[str, Any], int]:
        """Route to handle JWT Token refresh."""
        if token_header == None:
            return (
                {
                    "isSuccess": False,
                    "error": "No authorization header",
                },
                401,
            )

        token = token_header.split()[1]

        decoded = None

        try:
            decoded = jwt.decode(token, self.config["SECRET_KEY"], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return ({"isSuccess": False, "error": "JWT token has expired"}, 401)
        except Exception as e:
            return ({"isSuccess": False, "error": str(e)}, 500)

        if decoded == None:
            return ({"isSuccess": False, "error": "Error parsing JWT token."}, 500)

        # Required for converting to object.
        decoded["password"] = ""
        user = User.parse_obj(decoded)

        (new_token, refresh_token) = self.generateToken(user)

        return (
            {
                "isSuccess": True,
                "error": None,
                "token": new_token,
                "refresh": refresh_token,
            },
            200,
        )

    def checkhealth(self):
        """Route to handle health request."""
        return {"status": "OK"}

    def signup(self, user: User) -> Tuple[dict[str, Any], int]:
        """Route to handle user signup."""
        (id, errmsg, status_code) = self.db.add_user(user)

        if id == "":
            return (
                {
                    "isSuccess": False,
                    "error": errmsg,
                },
                int(status_code),
            )

        user_json = user.dict(exclude={"password"}, exclude_none=True)
        user_json["_id"] = str(id)

        return (
            {
                "isSuccess": True,
                "error": None,
                "payload": user_json,
            },
            200,
        )

    def login(self, user: User) -> Tuple[dict[str, Any], int]:
        """Route to handle user signin."""
        result = self.db.search_user(user)

        if result == None:
            return (
                {
                    "isSuccess": False,
                    "error": "User not found",
                },
                http.HTTPStatus.NOT_FOUND,
            )

        if result["password"] != user.password:
            return (
                {
                    "isSuccess": False,
                    "error": "email/password wrong.",
                },
                http.HTTPStatus.BAD_REQUEST,
            )

        (token, refresh) = self.generateToken(user)

        return (
            {
                "isSuccess": True,
                "error": None,
                "payload": user.dict(),
                "token": token,
                "refresh": refresh,
            },
            http.HTTPStatus.OK,
        )

    def generateToken(self, user: User) -> Tuple[str, str]:
        """Generate a pair of JWT Token."""
        payload = user.dict(exclude={"password"}, exclude_none=True)

        payload["exp"] = datetime.now() + timedelta(days=1)

        key = ""
        if "SECRET_KEY" in self.config:
            key = self.config["SECRET_KEY"]
        else:
            return ("", "")

        token = jwt.encode(payload=payload, key=key, algorithm="HS256")

        payload["exp"] = datetime.now() + timedelta(days=7)

        refresh = jwt.encode(payload=payload, key=key, algorithm="HS256")

        return (token, refresh)
