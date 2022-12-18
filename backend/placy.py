"""Module to define the application."""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
from backend import routes
from backend.database import DatabaseService
from backend.models import User
from backend.logging import LoggingService


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
            response = self.router.signup(user)
            return JSONResponse(status_code=response["status"], content=response)

        @self.app.post("/login", status_code=200)
        def login(user: User):
            response = self.router.login(user)
            return JSONResponse(status_code=response["status"], content=response)

    def run(self) -> None:
        """Run the app with given settings."""
        uvicorn.run(self.app, port=5000, log_level="info")
