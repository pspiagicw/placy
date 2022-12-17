"""Module for database services."""


class DatabaseService:
    """Superclass for injecting Database as a service into application."""

    pass


class MongoService(DatabaseService):
    """Implemented subclass to manage connection with MongoDB."""

    pass
