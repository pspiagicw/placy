"""ORM models for MongoDB."""

from mongoengine import BooleanField, Document, EmailField, ListField, StringField
from mongoengine.fields import DateTimeField


class User(Document):
    """Model for the user."""

    email = EmailField(required=True, unique=True)
    username = StringField(required=True, unique=True)
    role = StringField(default="user")

    created_at = DateTimeField(required=True)
    updated_at = DateTimeField(required=True)

    password = StringField(required=True)
    isBanned = BooleanField(default=False)


class OTP(Document):
    """Model for OTP."""

    email = EmailField(required=True, unique=True)
    otp = StringField(required=True)
    exp = DateTimeField(required=True)
