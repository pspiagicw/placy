"""Module to contain routes for communities."""

from fastapi import FastAPI
from fastapi.responses import Response
from placy.controllers.community import CommunityController
from placy.models.community import InputPost, InputComment
from placy.models.community_orm import Post
from placy.models.response import ErrorResponse


def setupCommunityRoutes(app: FastAPI, controller: CommunityController) -> None:
    """Configure routes for community."""

    @app.get(
        "/community/{community_id}",
        response_model=list[InputPost],
        response_description="List all posts",
    )
    def list_posts(temp: Response, community_id: str):
        response = controller.get_all_posts(community_id)
        temp.status_code = response.status_code
        return response

    @app.get(
        "/community/post/{post_id}",
        response_model=InputPost,
        response_description="Return a specific post.",
    )
    def get_post(temp: Response, post_id: str):
        response = controller.get_specific_post(post_id)
        temp.status_code = response.status_code
        return response

    @app.post(
        "/comment/add/{post_id}",
        response_model=ErrorResponse,
        response_description="Add a comment to a post.",
    )
    def add_comment(temp: Response, post_id: str, comment: InputComment):
        response = controller.add_comment(post_id, comment)
        temp.status_code = response.status_code
        return response
