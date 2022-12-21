"""Module for database services."""


from collections import namedtuple
from http import HTTPStatus
from typing import Any, Tuple

from mongoengine import connect
from mongoengine.errors import NotUniqueError
from placy.models.auth import Auth, PasswordUpdate
from placy.models.auth_orm import OTP, User
from pymongo import MongoClient

DatabaseResponse = namedtuple("DatabaseResponse", ["data", "errmsg", "status"])


class DatabaseService:
    """Superclass for injecting Database as a service into application."""

    def __init__(self) -> None:
        """Construct Database Service class."""
        pass

    def setup(self, config: dict[str, str | None]) -> None:
        """Initialize connection to database."""
        print(config)
        pass

    def add_user(self, user: User) -> DatabaseResponse:
        """Add user to the database."""
        print(user)
        return DatabaseResponse("", "", 0)

    def search_user(self, email: str) -> User | None:
        """Search user in the database."""
        print(email)
        return None

    def add_otp(self, otp: OTP) -> Tuple[str, str, int]:
        """Add OTP instance in the database."""
        print(otp)
        return ("", "", 0)

    def search_otp(self, update: PasswordUpdate) -> OTP | None:
        """Search for a OTP in the database."""
        print(update)
        return None

    def update_user_password(
        self, email: str, password: str, salt: str
    ) -> DatabaseResponse:
        """Update given user's password."""
        print(email)
        print(password)
        print(salt)
        return DatabaseResponse(data="", errmsg="", status=0)

    def delete_otp(self, update: PasswordUpdate) -> DatabaseResponse:
        """Delete a given OTP."""
        print(update)
        return DatabaseResponse(data="", errmsg="", status=0)


class MongoService(DatabaseService):
    """Implemented subclass to manage connection with MongoDB."""

    def __init__(self):
        """Construct the Mongo Service class."""
        self.client = None
        super().__init__()

    def setup(self, config: dict[str, str | None]) -> None:
        """Connect to MongoDB."""
        if config.get("MONGO_URI") == None:
            raise Exception("MONGO_URI is empty")

        connect(db="placy")

    def add_user(self, user: User) -> DatabaseResponse:
        """Add a user into MongoDB database."""
        response = None

        try:
            response = user.save(force_insert=True)
        except NotUniqueError:
            return DatabaseResponse(
                data="", errmsg="User already exists", status=HTTPStatus.CONFLICT
            )
        except Exception as e:
            return DatabaseResponse(
                data="", errmsg=str(e), status=HTTPStatus.INTERNAL_SERVER_ERROR
            )

        if response.id:
            return DatabaseResponse(data=id, errmsg="", status=HTTPStatus.CREATED)
        else:
            return DatabaseResponse(
                data="",
                errmsg="Error saving user to database.",
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

    def search_user(self, email: str) -> User | None:
        """Search for a given user in MongoDB database."""
        result = None

        try:
            result = User.objects.get(email=email)
        except:
            return None

        return result

    def add_otp(self, otp: OTP) -> DatabaseResponse:
        """Add the OTP instance to the MongoDB database."""
        response = None

        try:
            response = otp.save()
        except Exception as e:
            return DatabaseResponse(
                data="", errmsg=str(e), status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
        if response.id:
            return DatabaseResponse(data=id, errmsg="", status=HTTPStatus.CREATED)
        else:
            return DatabaseResponse(
                data="",
                errmsg="Error saving otp to database.",
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

    def search_otp(self, update: PasswordUpdate) -> OTP | None:
        """Search a given OTP."""
        result = None

        try:
            result = OTP.objects.get(email=update.email)
        except:
            return None

        return result

    def update_user_password(
        self, email: str, password: str, salt: str
    ) -> DatabaseResponse:
        """Update given user's password."""
        user = self.search_user(email)

        if user == None:
            return DatabaseResponse(
                status=HTTPStatus.NOT_FOUND, errmsg="User not found", data=""
            )

        user.password = password
        user.salt = salt

        response = None

        try:
            response = user.save()
        except Exception as e:
            return DatabaseResponse(
                data="", errmsg=str(e), status=HTTPStatus.INTERNAL_SERVER_ERROR
            )

        if response.id:
            return DatabaseResponse(data=id, errmsg="", status=HTTPStatus.CREATED)
        else:
            return DatabaseResponse(
                data="",
                errmsg="Error saving user to database.",
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
            )
