"""Module to contain models for authentication API."""

from pydantic import BaseModel


class Health(BaseModel):
    """Model to represent API health and info."""

    version: str
    client: str
