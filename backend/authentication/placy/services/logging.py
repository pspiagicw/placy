"""Module handles logging."""


import logging

from placy.services.config import Config


class LoggingService:
    """Superclass for injecting Logging as a service into application."""

    def __init__(self, config: Config) -> None:
        """Configure the logger."""
        self.config = config

    def setup(self) -> None:
        """Initialize logging service."""

    def log_info(self, data: str) -> None:
        """Log info data."""
        pass

    def log_error(self, data: str) -> None:
        """Log error data."""
        pass

    def log_warning(self, data: str) -> None:
        """Log warning data."""
        pass


class DefaultLogger(LoggingService):
    """Implemented subclass to manage logging."""

    def __init__(self, config: Config) -> None:
        """Log to a file.."""
        super().__init__(config)

    def setup(self) -> None:
        """Configure the default logger."""
        logging.basicConfig(filename=self.config.log_file, level=logging.INFO)

    def log_info(self, data: str) -> None:
        """Log info onto root logger."""
        logging.info(data)

    def log_warning(self, data: str) -> None:
        """Log warning onto root logger."""
        logging.warning(data)

    def log_error(self, data: str) -> None:
        """Log error onto root logger."""
        logging.error(data)
