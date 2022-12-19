"""Module for database services."""


from collections import namedtuple
from http import HTTPStatus
from typing import Any, Tuple

from placy.models.auth import OTP, Auth, Profile, User
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

    def add_user(self, user: User) -> Tuple[str, str, int]:
        """Add user to the database."""
        print(user)
        return ("", "", 0)

    def search_user(self, auth: Auth) -> User | None:
        """Search user in the database."""
        print(auth)
        return None

    def add_otp(self, otp: OTP) -> Tuple[str, str, int]:
        """Add OTP instance in the database."""
        print(otp)
        return ("", "", 0)

    def search_otp(self, email: str) -> OTP | None:
        """Search for a OTP in the database."""
        print(email)
        return None

    def update_user_profile(self, user: User, profile: Profile) -> DatabaseResponse:
        """Update given user's profile."""
        print(user)
        print(profile)
        return DatabaseResponse(data=False, errmsg="", status=0)


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

        self.client = MongoClient(config["MONGO_URI"])
        db = self.client["placy"]
        collection = db["users"]

        self.user_collection = collection

        db = self.client["placy"]
        collection = db["otp"]

        self.otp_collection = collection

    def update_user_profile(self, user: User, profile: Profile) -> DatabaseResponse:
        """Update details for a user."""
        if self.client == None:
            return DatabaseResponse(
                data="",
                errmsg="Mongo connection is null.",
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

        exists = self.search_user(user.auth)

        if not exists:
            return DatabaseResponse(
                data="", errmsg="User does not exist", status=HTTPStatus.NOT_FOUND
            )

        profile_payload = profile.dict()

        result = self.user_collection.update_one(
            filter={"auth.email": user.auth.email},
            update={"$set": {"profile": profile_payload}},
        )

        if result.modified_count == 1 and result.matched_count == 1:
            return DatabaseResponse(True, "", HTTPStatus.OK)

        return DatabaseResponse(
            False, "No documents found/modified", HTTPStatus.INTERNAL_SERVER_ERROR
        )

    def add_user(self, user: User) -> DatabaseResponse:
        """Add a user into MongoDB database."""
        if self.client == None:
            return DatabaseResponse(
                data="",
                errmsg="Mongo connection is null.",
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

        exists = self.search_user(user.auth)

        if exists:
            return DatabaseResponse(
                data="",
                errmsg="User with email already exists.",
                status=HTTPStatus.CONFLICT,
            )

        payload = user.dict()
        id = self.user_collection.insert_one(payload).inserted_id

        return DatabaseResponse(data=id, errmsg="", status=HTTPStatus.CREATED)

    def search_user(self, auth: Auth) -> User | None:
        """Search for a given user in MongoDB database."""
        if self.client == None:
            return None

        result = self.user_collection.find_one({"auth.email": auth.email})

        if result == None:
            return result

        user = User.parse_obj(result)

        return user

    def add_otp(self, otp: OTP) -> Tuple[str, str, int]:
        """Add the OTP instance to the MongoDB database."""
        if self.client == None:
            return (
                "",
                "Mongo connection is null.",
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )

        payload = otp.dict()
        id = self.otp_collection.insert_one(payload).inserted_id

        return (id, "", 200)
