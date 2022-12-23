"""Module contains models for authentication."""

import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field


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
