"""Module to route all backend requests."""

from placy.database import DatabaseService
from fastapi.encoders import jsonable_encoder
from placy.models import (
    OTP,
    Email,
    User,
    UpdatePassword,
    Auth,
    ErrorResponse,
    AuthResponse,
)
from typing import Any, Tuple
from http import HTTPStatus
import random
import jwt
from datetime import datetime, timedelta


class Router:
    """Router handles all routing."""

    def __init__(self, db: DatabaseService, config: dict[str, str]):
        """Construct the Router class."""
        self.db = db
        self.config = config

    def generate_hash(self, password: str) -> Tuple[str, str]:
        """Generate a hash and the salt to store."""
        salt = "".join([str(random.randint(0, 9)) for _ in range(6)])
        hash = password + salt

        return (salt, hash)

    def comparePasswords(self, givenPass: str, actualPass: str, salt: str) -> bool:
        """Compare passwords."""
        return givenPass + salt == actualPass

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

    def checkhealth(self, status: str):
        """Route to handle health request."""
        return {"status": "OK", "version": status}

    def signup(self, auth: Auth) -> AuthResponse | ErrorResponse:
        """Route to handle user signup."""
        (salt, hash_password) = self.generate_hash(auth.password)

        auth.password = hash_password
        auth.salt = salt

        user = User(
            auth=auth,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            profile_completed=False,
            profile=None,
        )

        (id, errmsg, status_code) = self.db.add_user(user)

        if id == "":
            return ErrorResponse(
                status=status_code,
                success=False,
                errmsg=errmsg,
            )

        user.auth.password = ""
        user.auth.salt = None

        return AuthResponse(
            status=200, success=True, error=None, payload=user, token=None, refresh=None
        )

    def login(self, auth: Auth) -> AuthResponse | ErrorResponse:
        """Route to handle user signin."""
        user = self.db.search_user(auth)

        if user == None:
            return ErrorResponse(
                success=False, errmsg="User not found", status=HTTPStatus.NOT_FOUND
            )

        if not self.comparePasswords(
            givenPass=auth.password,
            actualPass=user.auth.password,
            salt=user.auth.salt if user.auth.salt else "",
        ):
            return ErrorResponse(
                status=400, errmsg="email/password wrong", success=False
            )

        (token, refresh) = self.generateToken(user)

        if token == "":
            return ErrorResponse(
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
                success=False,
                errmsg="Can't generate token. SECRET_KEY empty.",
            )

        user.auth.password = ""
        user.auth.salt = ""

        return AuthResponse(
            status=HTTPStatus.OK,
            success=True,
            error=None,
            payload=user,
            token=token,
            refresh=refresh,
        )

    def generateToken(self, user: User) -> Tuple[str, str]:
        """Generate a pair of JWT Token."""
        payload = jsonable_encoder(user, exclude={"auth": {"password", "salt"}})

        payload["exp"] = str(datetime.now() + timedelta(days=1))

        key = ""
        if "SECRET_KEY" in self.config:
            key = self.config["SECRET_KEY"]
        else:
            return ("", "")

        token = jwt.encode(payload=payload, key=key, algorithm="HS256")

        payload["exp"] = str(datetime.now() + timedelta(days=7))

        refresh = jwt.encode(payload=payload, key=key, algorithm="HS256")

        return (token, refresh)
