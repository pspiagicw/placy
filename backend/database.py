"""Module for database services."""


from backend.models import User
from typing import Tuple
from pymongo import MongoClient
import http


class DatabaseService:
    """Superclass for injecting Database as a service into application."""

    def __init__(self) -> None:
        """Construct Database Service class."""
        pass

    def setup(self, config: dict[str, str | None]) -> None:
        """Initialize connection to database."""
        print(config)
        pass

    def add_user(self, user: User) -> str:
        """Add user to the database."""
        print(user)
        return ""

    def search_user(self, user: User) -> User | None:
        """Search user in the database."""
        print(user)
        return None


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

    def add_user(self, user: User) -> Tuple[str, str, int]:
        """Add a user into MongoDB database."""
        if self.client == None:
            return (
                "",
                "Mongo connection is null.",
                http.HTTPStatus.INTERNAL_SERVER_ERROR,
            )

        exists = self.search_user(user)

        if exists:
            return ("", "User with email already exists.", http.HTTPStatus.CONFLICT)

        payload = user.dict()
        id = self.user_collection.insert_one(payload).inserted_id

        return (id, "", http.HTTPStatus.CREATED)

    def search_user(self, user: User) -> User | None:
        """Search for a given user in MongoDB database."""
        if self.client == None:
            return None

        result = self.user_collection.find_one({"email": user.email})

        return result
