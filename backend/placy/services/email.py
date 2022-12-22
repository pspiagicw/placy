"""Module for conducting Email Services."""

import sendgrid
from placy.services.config import Config
from sendgrid.helpers.mail import Content, Email, Mail


class EmailService:
    """Superclass for Email Service."""

    def __init__(self, config: Config):
        """Construct a email Service."""
        self.config = config

    def send_email(self, email: str, otp: str):
        """Send a email."""
        print(email)
        print(otp)


class SendGridService(EmailService):
    """Subclass for emailing using SendGrid."""

    def __init__(self, config: Config):
        """Construct SendGridService class."""
        super().__init__(config)

    def send_email(self, email: str, otp: str):
        """Send email using SendGrid."""
        print("Sending email")
        # from_email = "pspiagicw@gmail.com"
        # to_email = email
        # subject = "A test email from Sendgrid"
        # content = f"Bitch here's your otp: {otp}"
        # print("Sending email")
        # mail = Mail(
        #     from_email=from_email,
        #     to_emails=to_email,
        #     subject=subject,
        #     html_content=content,
        # )
        #
        # response = None
        #
        # if "SENDGRID_API_KEY" not in self.config:
        #     print("API KEY missing!")
        #
        # try:
        #     print("Sending email")
        #     sg = sendgrid.SendGridAPIClient(self.config["SENDGRID_API_KEY"])
        #     print("Sending email")
        #     sg.send(mail)
        # except Exception as e:
        #     print(e)
