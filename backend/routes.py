"""Module to route all backend requests."""

from backend.database import DatabaseService


def checkhealth(db: DatabaseService, config: dict[str, str]):
    """Route to handle health request."""
    return {"status": "OK"}
