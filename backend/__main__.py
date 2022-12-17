"""Module to run backend."""

from backend.placy import Placy
from fastapi import FastAPI


if __name__ == "__main__":
    app = FastAPI()
    placy = Placy(app, None, {})
    placy.setup_routes()
    placy.run()
