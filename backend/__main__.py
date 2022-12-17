"""Module to run backend."""

from backend.database import MongoService
from backend.placy import Placy
from fastapi import FastAPI
from dotenv import dotenv_values
from backend.routes import Router
from backend.logging import DefaultLogger


if __name__ == "__main__":
    app = FastAPI()
    config = dotenv_values()
    database = MongoService()
    router = Router(database, config)
    logger = DefaultLogger()
    placy = Placy(
        app=app,
        databaseService=database,
        loggingService=logger,
        config=config,
        router=router,
    )
    placy.setup()
    placy.routes()
    placy.run()
