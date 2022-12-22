"""Config Service."""


from datetime import timedelta


class Config:
    """Config Service."""

    def __init__(
        self,
        mongo_uri: str,
        sendgrid_api_key: str,
        secret_key: str = "someusefulpassword",
    ):
        """Construct the ConfigService Class."""
        if mongo_uri == "":
            raise ValueError("MONGO URI empty.")
        if sendgrid_api_key == "":
            raise ValueError("SENDGRID_API_KEY empty.")

        self.mongo_uri = mongo_uri
        self.secret_key = secret_key
        self.sendgrid_api_key = sendgrid_api_key
        self.otp_expiry = timedelta(minutes=15)
        self.token_expiry = timedelta(days=1)
        self.refresh_expiry = timedelta(days=7)
        self.jwt_algorithms = ["HS256"]
        self.jwt_algorithm = "HS256"
