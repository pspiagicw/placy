"""Configure routes for authentication."""

from fastapi import FastAPI, Header, Response
from placy.controllers.auth import AuthController
from placy.models.auth import Auth
from placy.models.response import AuthResponse, ErrorResponse, JWTRefreshResponse
from pydantic import EmailStr


def setupAuthRoutes(app: FastAPI, controller: AuthController) -> None:
    """Configure routes for authentication."""

    @app.post(
        "/auth/signup",
        response_model=AuthResponse | ErrorResponse,
        response_model_exclude_none=True,
        response_description="Allowr user signup.",
    )
    def signup(auth: Auth, temp: Response):
        response = controller.signup(auth)
        temp.status_code = response.status
        return response

    @app.post(
        "/auth/login",
        response_model=AuthResponse | ErrorResponse,
        response_model_exclude_none=True,
        response_description="Allows user logins.",
    )
    def login(auth: Auth, temp: Response):
        response = controller.login(auth)
        temp.status_code = response.status
        return response

    @app.get(
        "/auth/refresh",
        response_model=JWTRefreshResponse | ErrorResponse,
        response_description="Allows refreshing JWT token.",
    )
    def refresh(temp: Response, authorization: str | None = Header(default=None)):
        response = controller.refresh(authorization)
        temp.status_code = response.status
        return response

    @app.post(
        "/auth/forgot",
        response_model=ErrorResponse,
        response_description="Allows user to request forgot password.",
    )
    def forgot(email: EmailStr, temp: Response):
        response = controller.forgot(email)
        temp.status_code = response.status
        return response

    # @app.post("/reset")
    # def reset(update: UpdatePassword):
    #     (response, status_code) = controller.reset(update)
    #     return JSONResponse(status_code=status_code, content=response)
