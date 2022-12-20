"""Module for conducting Email Services."""


class EmailService:
    """Superclass for Email Service."""

    def __init__(self, config: dict[str, str]):
        """Construct a email Service."""
        self.config = config

    def send_email(self, email: str, otp: str):
        """Send a email."""
        print(email)
        print(otp)


# class AWSEmailer:
