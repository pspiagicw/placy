"""Module has controllers for Authentication."""

import random
from collections import namedtuple
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Tuple

import jwt
from fastapi.encoders import jsonable_encoder
from placy.models.auth import OTP, Auth, Profile, UpdatePassword, User
from placy.models.response import (
    AuthResponse,
    ErrorResponse,
    Health,
    JWTRefreshResponse,
)
from placy.services.database import DatabaseService
from placy.services.email import EmailService
from pydantic import EmailStr

TokenResponse = namedtuple("TokenResponse", ["user", "error"])


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

        instance = OTP(email=EmailStr(email), otp=otp, exp=exp, used=False)
        return instance

    def reset(self, update: UpdatePassword) -> ErrorResponse:
        """Route to handle reset password requests."""
        otp = self.db.search_otp(update)

        if otp == None:
            return ErrorResponse(
                status=HTTPStatus.BAD_REQUEST, success=False, errmsg="OTP not found."
            )

        now = datetime.now()

        if otp.exp < now:
            return ErrorResponse(
                status=HTTPStatus.BAD_REQUEST, success=False, errmsg="OTP has expired."
            )

        result = self.db.delete_otp(update)

        if result.status != HTTPStatus.OK:
            return ErrorResponse(
                status=result.status, success=False, errmsg=result.errmsg
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

        self.email.send_email(email, otp.otp)

        return ErrorResponse(success=True, errmsg="null", status=HTTPStatus.OK)

    def refresh(self, token_header: str | None) -> ErrorResponse | JWTRefreshResponse:
        """Route to handle JWT Token refresh."""
        if token_header == None:
            return ErrorResponse(
                status=HTTPStatus.UNAUTHORIZED,
                success=False,
                errmsg="No authorization header.",
            )

        (user, error) = self.confirmToken(token_header=token_header)

        if user == None or error != None:
            return error

        (new_token, refresh_token) = self.generateToken(user)

        return JWTRefreshResponse(
            status=HTTPStatus.OK, success=True, token=new_token, refresh=refresh_token
        )

    def checkhealth(self, status: str):
        """Route to handle health request."""
        return Health(status="OK", version=0.1)

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
        foundUser = self.db.search_user(auth)

        if foundUser == None:
            return ErrorResponse(
                success=False, errmsg="User not found", status=HTTPStatus.NOT_FOUND
            )

        if not self.comparePasswords(
            givenPass=auth.password,
            actualPass=foundUser.auth.password,
            salt=foundUser.auth.salt if foundUser.auth.salt else "",
        ):
            return ErrorResponse(
                status=400, errmsg="email/password wrong", success=False
            )

        (token, refresh) = self.generateToken(foundUser)

        if token == "":
            return ErrorResponse(
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
                success=False,
                errmsg="Can't generate token. SECRET_KEY empty.",
            )

        foundUser.auth.password = ""
        foundUser.auth.salt = ""

        return AuthResponse(
            status=HTTPStatus.OK,
            success=True,
            error=None,
            payload=foundUser,
            token=token,
            refresh=refresh,
        )

    def generateToken(self, user: User) -> Tuple[str, str]:
        """Generate a pair of JWT Token."""
        payload = jsonable_encoder(user, exclude={"auth": {"password", "salt"}})

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

    def profile(self, profile: Profile, authorization: str | None) -> ErrorResponse:
        """Update the profile for the user."""
        if authorization == None:
            return ErrorResponse(
                status=HTTPStatus.BAD_REQUEST,
                success=False,
                errmsg="Authorization token absent.",
            )

        response = self.confirmToken(authorization)

        if response.error != None:
            return response.error

        (result, errmsg, status) = self.db.update_user_profile(response.user, profile)

        if result == False:
            return ErrorResponse(success=False, status=status, errmsg=errmsg)

        return ErrorResponse(success=True, status=status, errmsg=errmsg)

    def confirmToken(self, token_header: str) -> TokenResponse:
        """Decode the JWT token and return the body."""
        token = token_header.split()[1]
        decoded = None

        try:
            decoded = jwt.decode(token, self.config["SECRET_KEY"], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return TokenResponse(
                user=None,
                error=ErrorResponse(
                    success=False,
                    errmsg="JWT token has expired",
                    status=HTTPStatus.UNAUTHORIZED,
                ),
            )

        except Exception as e:
            return TokenResponse(
                user=None,
                error=ErrorResponse(
                    success=False,
                    errmsg=str(e),
                    status=HTTPStatus.INTERNAL_SERVER_ERROR,
                ),
            )

        if decoded == None:
            return TokenResponse(
                user=None,
                error=ErrorResponse(
                    success=False,
                    errmsg="Error parsing JWT token.",
                    status=HTTPStatus.INTERNAL_SERVER_ERROR,
                ),
            )

        # Required for converting to object.
        decoded["auth"]["password"] = ""
        user = User.parse_obj(decoded)

        return TokenResponse(user=user, error=None)
