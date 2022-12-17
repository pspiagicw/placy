"""Module handles logging."""


import logging


class LoggingService:
    """Superclass for injecting Logging as a service into application."""

    def setup(self, config: dict[str, str]) -> None:
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

    def log_info(self, data: str) -> None:
        """Log info onto root logger."""
        logging.info(data)

    def log_warning(self, data: str) -> None:
        """Log warning onto root logger."""
        logging.warning(data)

    def log_error(self, data: str) -> None:
        """Log error onto root logger."""
        logging.error(data)
