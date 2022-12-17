"""Module to define the application."""

from fastapi import FastAPI
import uvicorn
from backend import routes
from backend.database import DatabaseService


class Placy:
    """Application initializes the backend, with a database service and other stuff."""

    def __init__(
        self, app: FastAPI, databaseService: DatabaseService, config: dict[str, str]
    ) -> None:
        """Construct for the Application class."""
        self.db_service = databaseService
        self.app = app
        self.config = config

    def setup_routes(self) -> None:
        """Route all requests."""
        dependencies = {"config": self.config, "db": DatabaseService}

        @self.app.get("/health")
        def checkhealth():
            return routes.checkhealth(**dependencies)

    def run(self) -> None:
        """Run the app with given settings."""
        uvicorn.run(self.app, port=5000, log_level="info")
