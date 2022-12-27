"""Module for database services."""


from collections import namedtuple
from http import HTTPStatus
from typing import Tuple

from mongoengine import connect
from mongoengine.errors import NotUniqueError
from placy.models.auth import PasswordUpdate
from placy.models.auth_orm import OTP, User
from placy.services.config import Config
from placy.services.logging import LoggingService

DatabaseResponse = namedtuple("DatabaseResponse", ["data", "errmsg", "status"])


class DatabaseService:
    """Superclass for injecting Database as a service into application."""

    def __init__(self) -> None:
        """Construct Database Service class."""
        pass

    def setup(self) -> None:
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

    def search_otp(self, email: str) -> OTP | None:
        """Search for a OTP in the database."""
        print(email)
        return None

    def update_user_password(self, email: str, password: str) -> DatabaseResponse:
        """Update given user's password."""
        print(email)
        print(password)
        return DatabaseResponse(data="", errmsg="", status=0)

    def delete_otp(self, update: PasswordUpdate) -> DatabaseResponse:
        """Delete a given OTP."""
        print(update)
        return DatabaseResponse(data="", errmsg="", status=0)


class MongoService(DatabaseService):
    """Implemented subclass to manage connection with MongoDB."""

    def __init__(self, logger: LoggingService):
        """Construct the Mongo Service class."""
        self.logger = logger
        super().__init__()

    def setup(self) -> None:
        """Connect to MongoDB."""
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
        user = self.search_user(str(otp.email))

        if user == None:
            return DatabaseResponse(
                data="",
                errmsg="User with email does not exist",
                status=HTTPStatus.NOT_FOUND,
            )

        found_otp = self.search_otp(str(otp.email))

        # OTP already exists, try to overwrite.
        # Or else it gives key not unique error.
        if found_otp != None:
            found_otp.otp = otp.otp
            found_otp.exp = otp.exp
            otp = found_otp

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

    def search_otp(self, email: str) -> OTP | None:
        """Search a given OTP."""
        result = None

        try:
            result = OTP.objects.get(email=email)
        except:
            return None

        return result

    def update_user_password(self, email: str, password: str) -> DatabaseResponse:
        """Update given user's password."""
        user = self.search_user(email)

        if user == None:
            return DatabaseResponse(
                status=HTTPStatus.NOT_FOUND, errmsg="User not found", data=""
            )

        user.password = password

        response = None

        try:
            response = user.save()
        except Exception as e:
            return DatabaseResponse(
                data="", errmsg=str(e), status=HTTPStatus.INTERNAL_SERVER_ERROR
            )

        if response.id:
            return DatabaseResponse(data=id, errmsg="", status=HTTPStatus.NO_CONTENT)
        else:
            return DatabaseResponse(
                data="",
                errmsg="Error saving user to database.",
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
            )
