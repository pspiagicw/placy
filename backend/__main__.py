"""Module to run backend."""

from backend.database import MongoService
from backend.placy import Placy
from fastapi import FastAPI
from dotenv import dotenv_values
from backend.routes import Router


if __name__ == "__main__":
    app = FastAPI()
    config = dotenv_values()
    database = MongoService()
    router = Router(database, config)
    placy = Placy(app, database, config, router)
    placy.setup()
    placy.routes()
    placy.run()
