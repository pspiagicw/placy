"""Module for conducting Email Services."""

import sendgrid
from placy.services.config import Config
from placy.services.logging import LoggingService
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

    def __init__(self, config: Config, logging: LoggingService):
        """Construct SendGridService class."""
        super().__init__(config)
        self.logging = logging

    def send_email(self, email: str, otp: str):
        """Send email using SendGrid."""
        from_email = "pspiagicw@gmail.com"
        to_email = email
        subject = "A test email from Sendgrid"
        content = f"Bitch here's your otp: {otp}"

        self.logging.log_info("All mail details confirmed.")

        mail = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=subject,
            html_content=content,
        )

        response = None

        try:
            self.logging.log_info("About to initialize SENDGRID API Client.")
            sg = sendgrid.SendGridAPIClient(self.config.sendgrid_api_key)
            self.logging.log_info("API Client initialized, sending email...")
            sg.send(mail)
            self.logging.log_info("Email Sent!")
        except Exception as e:
            self.logging.log_error(f"Some error occured while sending mail: {str(e)}")
