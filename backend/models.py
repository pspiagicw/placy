"""Module to contain models for API."""

from pydantic import BaseModel


class Health(BaseModel):
    """Model to represent API health and info."""

    version: str
    client: str


class User(BaseModel):
    """Model for user."""

    name: str
    username: str
    email: str
    password: str
    phone_no: int
    branch: str
    year: int
    gpa: float
