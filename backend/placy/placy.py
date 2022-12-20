"""Module to define the application."""

from fastapi import FastAPI
from fastapi import Header
from fastapi.responses import JSONResponse
import uvicorn
from placy import routes
from placy.database import DatabaseService
from placy.models import UpdatePassword, User, Email
from placy.logging import LoggingService


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

        @self.app.get("/health")
        def health():
            response = self.router.checkhealth()
            return response

        @self.app.post("/signup", status_code=201)
        def signup(user: User):
            (response, status_code) = self.router.signup(user)
            return JSONResponse(status_code=status_code, content=response)

        @self.app.post("/login", status_code=200)
        def login(user: User):
            (response, status_code) = self.router.login(user)
            return JSONResponse(status_code=status_code, content=response)

        @self.app.get("/refresh")
        def refresh(authorization: str | None = Header(default=None)):
            (response, status_code) = self.router.refresh(authorization)
            return JSONResponse(status_code=status_code, content=response)

        @self.app.post("/forgot")
        def forgot(email: Email):
            (response, status_code) = self.router.forgot(email)
            return JSONResponse(status_code=status_code, content=response)

        @self.app.post("/reset")
        def reset(update: UpdatePassword):
            (response, status_code) = self.router.reset(update)
            return JSONResponse(status_code=status_code, content=response)

    def run(self) -> None:
        """Run the app with given settings."""
        uvicorn.run(self.app, port=5000, log_level="info", host="0.0.0.0")
