"""Module to contain models for back API."""

from enum import Enum
from pydantic import BaseModel, EmailStr, Field
import datetime


class JWTRefreshResponse(BaseModel):
    """Model for JWT Refresh request."""

    status: int
    success: bool
    token: str
    refresh: str


class Health(BaseModel):
    """Model for health info."""

    status: str
    version: float


class ErrorResponse(BaseModel):
    """Model for containing response."""

    status: int
    success: bool
    errmsg: str


class RoleEnum(str, Enum):
    """Enum to contain roles."""

    user = "user"
    officer = "officir"
    moderator = "moderator"
    admin = "admin"


class UpdatePassword(BaseModel):
    """Model for updated password."""

    email: EmailStr
    otp: str = Field(max_length=6, min_length=6)
    new_password: str


class OTP(BaseModel):
    """Model to store OTP system."""

    email: EmailStr
    otp: str = Field(max_length=6, min_length=6)
    exp: datetime.datetime
    used: bool


class Auth(BaseModel):
    """Model for the user."""

    username: str
    email: EmailStr
    role: RoleEnum
    password: str
    salt: str | None


class Profile(BaseModel):
    """Model for Profile."""

    name: str
    year: int
    gpa: float
    communities: list[str]
    reputation: float
    isBanned: bool


class User(BaseModel):
    """Model for the user."""

    auth: Auth
    created_at: datetime.datetime
    updated_at: datetime.datetime
    profile_completed: bool

    profile: Profile | None


class AuthResponse(BaseModel):
    """Model for responding auth requests."""

    status: int
    success: bool
    error: str | None
    payload: User
    token: str | None
    refresh: str | None
