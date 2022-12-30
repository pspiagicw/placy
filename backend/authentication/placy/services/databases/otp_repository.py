"""OTP Repostory."""

from collections import namedtuple
from http import HTTPStatus

from mongoengine import connect
from placy.models.auth_orm import OTP
from placy.services.config import Config
from placy.services.databases.auth_repository import AuthRepository
from placy.services.logging import LoggingService

DatabaseResponse = namedtuple("DatabaseResponse", ["status", "data", "errmsg"])


class OTPRepository:
    """Repository for OTP."""

    def __init__(
        self, logger: LoggingService, authRepo: AuthRepository, config: Config
    ):
        """Construct the OTP Repostory."""
        self.logger = logger
        self.auth_repo = authRepo
        self.config = config

    def setup(self) -> None:
        """Connect to MongoDB."""
        connection_url = self.config.mongo_uri + "/placy"
        connect(db="placy")

    def add_otp(self, otp: OTP) -> DatabaseResponse:
        """Add the OTP instance to the MongoDB database."""
        user = self.auth_repo.search_user(str(otp.email))

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
