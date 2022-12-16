"""Module to contain models for API."""

from pydantic import BaseModel


class Health(BaseModel):
    """Model to represent API health and info."""

    version: str
    client: str
