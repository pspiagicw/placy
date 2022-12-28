"""Module to run backend."""

from dotenv import dotenv_values
from fastapi import FastAPI
from placy.controllers.auth import AuthController
from placy.services.config import Config
from placy.services.databases.auth_repository import AuthRepository
from placy.services.databases.community_repo import CommunityRepository
from placy.controllers.community import CommunityController
from placy.services.databases.otp_repository import OTPRepository
from placy.services.email import SendGridService
from placy.services.logging import DefaultLogger

from placy.placy import Placy

if __name__ == "__main__":
    app = FastAPI()
    env = dotenv_values()
    config = Config(
        mongo_uri=env["MONGO_URI"] if "MONGO_URI" in env else "",
        sendgrid_api_key=env["SENDGRID_API_KEY"] if "SENDGRID_API_KEY" in env else "",
    )
    logger = DefaultLogger(config)
    auth_repo = AuthRepository(logger)
    otp_repo = OTPRepository(authRepo=auth_repo, logger=logger)
    community_repo = CommunityRepository()
    email = SendGridService(config, logger)
    auth_controller = AuthController(
        otp_repo=otp_repo,
        auth_repo=auth_repo,
        config=config,
        emailService=email,
        logging=logger,
    )
    community_controller = CommunityController(
        logging=logger, community_repo=community_repo
    )
    placy = Placy(
        communityRepo=community_repo,
        communityController=community_controller,
        authRepo=auth_repo,
        otpRepo=otp_repo,
        app=app,
        loggingService=logger,
        config=config,
        authController=auth_controller,
        emailService=email,
    )
    placy.setup()
    placy.routes()
    placy.run()
