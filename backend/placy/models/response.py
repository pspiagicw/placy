"""Module contains models for responses."""
from placy.models.auth import Auth
from pydantic import BaseModel


class JWTRefreshResponse(BaseModel):
    """Model for JWT Refresh request."""

    status: int
    success: bool
    token: str
    refresh: str


class ErrorResponse(BaseModel):
    """Model for containing response."""

    status: int
    success: bool
    errmsg: str


class AuthResponse(BaseModel):
    """Model for responding auth requests."""

    status: int
    success: bool
    error: str | None
    payload: Auth
    token: str | None
    refresh: str | None


class Health(BaseModel):
    """Model for health info."""

    status: str
    version: float
