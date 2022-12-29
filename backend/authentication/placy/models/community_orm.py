"""Module contains models for ORM for Communities."""

from mongoengine import Document
from mongoengine.fields import (
    DateTimeField,
    ListField,
    ObjectIdField,
    ReferenceField,
    StringField,
)
from placy.models.auth_orm import User


class Comment(Document):
    """Comment Document."""

    author = ReferenceField(User)
    parentComment = ObjectIdField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    content = StringField(
        required=True,
        max_length=250,
    )
    subcomments = ListField(field=ObjectIdField)


class Post(Document):
    """Post Document."""

    title = StringField(required=True)
    moderationStatus = StringField(choices=("approved", "unseen", "rejected"))
    likedBy = ListField(ReferenceField(User))
    author = StringField(required=True)
    content = StringField(max_length=1000)
    comments = ListField(field=ReferenceField(Comment))
    moderators = ListField(field=ReferenceField(User))
    created_at = DateTimeField(required=True)
    updated_at = DateTimeField(required=True)


class Community(Document):
    """Communities Document."""

    name = StringField(required=True)
    description = StringField(required=True)
    posts = ListField(field=ReferenceField(Post))
    created_at = DateTimeField(required=True)
