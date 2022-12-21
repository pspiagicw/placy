"""Module has controllers for Authentication."""

import random
from collections import namedtuple
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Any, Tuple

import jwt
from fastapi.encoders import jsonable_encoder
from mongoengine.fields import dateutil
from placy.models.auth import Auth, PasswordUpdate
from placy.models.auth_orm import OTP, User
from placy.models.response import (
    AuthResponse,
    ErrorResponse,
    Health,
    JWTRefreshResponse,
)
from placy.services.database import DatabaseService
from placy.services.email import EmailService
from pydantic import EmailStr

TokenResponse = namedtuple("TokenResponse", ["confirmed", "error"])


class AuthController:
    """Router handles all routing."""

    def __init__(
        self, db: DatabaseService, config: dict[str, str], email: EmailService
    ):
        """Construct the Router class."""
        self.db = db
        self.config = config
        self.email = email

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

        instance = OTP(email=EmailStr(email), otp=otp, exp=exp)

        return instance

    def reset(self, update: PasswordUpdate) -> ErrorResponse:
        """Route to handle reset password requests."""
        otp = self.db.search_otp(update)

        if otp == None:
            return ErrorResponse(
                status=HTTPStatus.BAD_REQUEST, success=False, errmsg="OTP not found."
            )

        now = datetime.now()
        exp = dateutil.parser.parse(str(otp.exp))

        if exp < now:
            return ErrorResponse(
                status=HTTPStatus.BAD_REQUEST, success=False, errmsg="OTP has expired."
            )

        (salt, hash) = self.generate_hash(update.new_password)

        result = self.db.update_user_password(
            email=update.email, password=hash, salt=salt
        )

        if result.status != HTTPStatus.OK:
            return ErrorResponse(
                status=result.status, errmsg=result.errmsg, success=False
            )

        return ErrorResponse(status=result.status, errmsg="", success=True)

    def forgot(self, email: EmailStr) -> ErrorResponse:
        """Route to handle forgot password requests."""
        otp = self.generate_otp(email)

        (id, errmsg, status_code) = self.db.add_otp(otp)

        if id == "":
            return ErrorResponse(success=False, errmsg=errmsg, status=status_code)

        # self.email.send_email(email, otp.otp)

        return ErrorResponse(success=True, errmsg="null", status=HTTPStatus.OK)

    def checkhealth(self, status: str):
        """Route to handle health request."""
        return Health(status="OK", version=0.1)

    def refresh(self, token_header: str | None) -> ErrorResponse | JWTRefreshResponse:
        """Route to handle JWT Token refresh."""
        if token_header == None:
            return ErrorResponse(
                status=HTTPStatus.UNAUTHORIZED,
                success=False,
                errmsg="No authorization header.",
            )

        (auth, error) = self.decodeToken(token_header=token_header)

        if not auth and error:
            return error

        (new_token, refresh_token) = self.generateToken(auth)

        return JWTRefreshResponse(
            status=HTTPStatus.OK, success=True, token=new_token, refresh=refresh_token
        )

    def signup(self, auth: Auth) -> AuthResponse | ErrorResponse:
        """Route to handle user signup."""
        (salt, hash_password) = self.generate_hash(auth.password)

        user = User(
            email=auth.email,
            username=auth.username,
            password=hash_password,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            salt=salt,
        )

        db_response = self.db.add_user(user)

        if db_response.status == HTTPStatus.OK:
            return ErrorResponse(
                status=db_response.status,
                success=False,
                errmsg=db_response.errmsg,
            )

        return AuthResponse(
            status=200, success=True, error=None, payload=auth, token=None, refresh=None
        )

    def login(self, auth: Auth) -> AuthResponse | ErrorResponse:
        """Route to handle user signin."""
        foundUser = self.db.search_user(auth.email)

        if foundUser == None:
            return ErrorResponse(
                success=False, errmsg="User not found", status=HTTPStatus.NOT_FOUND
            )

        if not self.comparePasswords(
            givenPass=auth.password,
            actualPass=foundUser.password,
            salt=foundUser.salt,
        ):
            return ErrorResponse(
                status=400, errmsg="email/password wrong", success=False
            )

        (token, refresh) = self.generateToken(auth.dict(exclude={"password"}))

        if token == "":
            return ErrorResponse(
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
                success=False,
                errmsg="Can't generate token. SECRET_KEY empty.",
            )

        return AuthResponse(
            status=HTTPStatus.OK,
            success=True,
            error=None,
            payload=auth,
            token=token,
            refresh=refresh,
        )

    def generateToken(self, payload: dict[str, Any]) -> Tuple[str, str]:
        """Generate a pair of JWT Token."""
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

    def decodeToken(self, token_header: str) -> TokenResponse:
        """Decode the JWT token and return the body."""
        token = token_header.split()[1]
        decoded = None

        try:
            decoded = jwt.decode(token, self.config["SECRET_KEY"], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return TokenResponse(
                confirmed=False,
                error=ErrorResponse(
                    success=False,
                    errmsg="JWT token has expired",
                    status=HTTPStatus.UNAUTHORIZED,
                ),
            )
        except Exception as e:
            return TokenResponse(
                confirmed=False,
                error=ErrorResponse(
                    success=False,
                    errmsg=str(e),
                    status=HTTPStatus.INTERNAL_SERVER_ERROR,
                ),
            )

        return TokenResponse(confirmed=decoded, error=None)
