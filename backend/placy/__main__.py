"""Module to run backend."""

from dotenv import dotenv_values
from fastapi import FastAPI
from placy.controllers.auth import AuthController
from placy.services.config import Config
from placy.services.database import MongoService
from placy.services.email import SendGridService
from placy.services.logging import DefaultLogger

from placy.placy import Placy

if __name__ == "__main__":
    app = FastAPI()
    env = dotenv_values()
    config = Config(
        mongo_uri=env["MONGO_URI"],
        sendgrid_api_key=env["SENDGRID_API_KEY"],
    )
    database = MongoService()
    email = SendGridService(config)
    router = AuthController(database, config, email=email)
    logger = DefaultLogger()
    placy = Placy(
        app=app,
        databaseService=database,
        loggingService=logger,
        config=config,
        authController=router,
        emailService=email,
    )
    placy.setup()
    placy.routes()
    placy.run()
