"""Module to define the application."""

import uvicorn
from fastapi import FastAPI
from fastapi import Response as Response
from placy.controllers.auth import AuthController
from placy.models.response import Health
from placy.routes.auth import setupAuthRoutes
from placy.services.database import DatabaseService
from placy.services.email import EmailService
from placy.services.logging import LoggingService


class Placy:
    """Application initializes the backend, with a database service and other stuff."""

    def __init__(
        self,
        app: FastAPI,
        databaseService: DatabaseService,
        loggingService: LoggingService,
        emailService: EmailService,
        config: dict[str, str | None],
        authController: AuthController,
    ) -> None:
        """Construct for the Application class."""
        self.db_service = databaseService
        self.app = app
        self.config = config
        self.logging_service = loggingService
        self.authController = authController

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
            response = self.authController.checkhealth(self.app.version)
            return response

        setupAuthRoutes(app=self.app, controller=self.authController)

    def run(self) -> None:
        """Run the app with given settings."""
        uvicorn.run(self.app, port=5000, log_level="info", host="0.0.0.0")
