"""Auth Repository."""

from collections import namedtuple
from http import HTTPStatus

from mongoengine import connect
from mongoengine.errors import NotUniqueError
from placy.models.auth_orm import User
from placy.services.logging import LoggingService

DatabaseResponse = namedtuple("DatabaseResponse", ["status", "errmsg", "data"])


class AuthRepository:
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
