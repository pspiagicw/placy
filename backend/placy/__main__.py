"""Module to run backend."""

from dotenv import dotenv_values
from fastapi import FastAPI
from placy.controllers.auth import AuthController
from placy.services.database import MongoService
from placy.services.logging import DefaultLogger

from placy.placy import Placy

if __name__ == "__main__":
    app = FastAPI()
    config = dotenv_values()
    database = MongoService()
    router = AuthController(database, config)
    logger = DefaultLogger()
    placy = Placy(
        app=app,
        databaseService=database,
        loggingService=logger,
        config=config,
        authController=router,
    )
    placy.setup()
    placy.routes()
    placy.run()
