"""Module to define the application."""

from fastapi import FastAPI
from fastapi import Header
from fastapi.responses import JSONResponse
from pydantic import EmailStr
import uvicorn
from placy import routes
from placy.database import DatabaseService
from placy.models import (
    Health,
    JWTRefreshResponse,
    UpdatePassword,
    Auth,
    AuthResponse,
    ErrorResponse,
)
from placy.logging import LoggingService
from fastapi import Response as Response


class Placy:
    """Application initializes the backend, with a database service and other stuff."""

    def __init__(
        self,
        app: FastAPI,
        databaseService: DatabaseService,
        loggingService: LoggingService,
        config: dict[str, str | None],
        router: routes.Router,
    ) -> None:
        """Construct for the Application class."""
        self.db_service = databaseService
        self.app = app
        self.config = config
        self.router = router
        self.logging_service = loggingService

    def setup(self) -> None:
        """Perform initialization for backend application."""
        self.db_service.setup(self.config)
        self.logging_service.setup(self.config)

    def routes(self) -> None:
        """Route all requests."""

        @self.app.get(
            "/health",
            response_model=Health,
            response_description="Check the health of the server.",
        )
        def health():
            response = self.router.checkhealth(self.app.version)
            return response

        @self.app.post(
            "/signup",
            response_model=AuthResponse | ErrorResponse,
            response_model_exclude_none=True,
            response_description="Allowr user signup.",
        )
        def signup(auth: Auth, temp: Response):
            response = self.router.signup(auth)
            temp.status_code = response.status
            return response

        @self.app.post(
            "/login",
            response_model=AuthResponse | ErrorResponse,
            response_model_exclude_none=True,
            response_description="Allows user logins.",
        )
        def login(auth: Auth, temp: Response):
            response = self.router.login(auth)
            temp.status_code = response.status
            return response

        @self.app.get(
            "/refresh",
            response_model=JWTRefreshResponse | ErrorResponse,
            response_description="Allows refreshing JWT token.",
        )
        def refresh(temp: Response, authorization: str | None = Header(default=None)):
            response = self.router.refresh(authorization)
            temp.status_code = response.status
            return response

        @self.app.post(
            "/forgot",
            response_model=ErrorResponse,
            response_description="Allows user to request forgot password.",
        )
        def forgot(email: EmailStr, temp: Response):
            response = self.router.forgot(email)
            temp.status_code = response.status
            return response

        @self.app.post("/reset")
        def reset(update: UpdatePassword):
            (response, status_code) = self.router.reset(update)
            return JSONResponse(status_code=status_code, content=response)

    def run(self) -> None:
        """Run the app with given settings."""
        uvicorn.run(self.app, port=5000, log_level="info", host="0.0.0.0")
