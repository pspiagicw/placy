"""Community controllers."""


from placy.services.databases.community_repo import CommunityRepository
from placy.services.logging import LoggingService


class CommunityController:
    """Community Controller."""

    def __init__(self, logging: LoggingService, community_repo: CommunityRepository):
        """Construct the Community controller."""
        pass
