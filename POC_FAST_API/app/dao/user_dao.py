import logging
from typing import Optional, List

from app.models.user import User

logger = logging.getLogger(__name__)


class UserDAO:
    """DAO layer for user data access.

    This implementation uses in-memory constants. It can be replaced later
    with database, external REST API, cache, or enterprise directory access.
    """

    _USERS = {
        10001: User(
            id=10001,
            first_name="Promit",
            last_name="Majumder",
            email="promit.majumder@example.com",
            role="Lead Software Engineer",
            department="Engineering",
            active=True,
        ),
        10002: User(
            id=10002,
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            role="Product Manager",
            department="Product",
            active=True,
        ),
        10003: User(
            id=10003,
            first_name="Rahul",
            last_name="Sharma",
            email="rahul.sharma@example.com",
            role="QA Engineer",
            department="Quality Engineering",
            active=False,
        ),
    }

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        logger.debug("Fetching user from DAO for user_id=%s", user_id)
        return self._USERS.get(user_id)

    def get_all_users(self) -> List[User]:
        """Return all users as a list."""
        logger.debug("Fetching all users from DAO")
        return list(self._USERS.values())
