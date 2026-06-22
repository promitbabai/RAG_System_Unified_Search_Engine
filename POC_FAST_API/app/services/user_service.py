import logging

from app.dao.user_dao import UserDAO
from app.exceptions.custom_exceptions import UserNotFoundException
from app.models.user import User

logger = logging.getLogger(__name__)


class UserService:
    """Service layer for user-related business logic."""

    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao

    def get_user_details(self, user_id: int) -> User:
        logger.info("Processing request to get user details for user_id=%s", user_id)

        user = self.user_dao.get_user_by_id(user_id)

        if user is None:
            logger.warning("User not found for user_id=%s", user_id)
            raise UserNotFoundException(user_id=user_id)

        logger.info("User found for user_id=%s", user_id)
        return user

    def get_all_users(self) -> list[User]:
        logger.info("Processing request to get all users")
        users = self.user_dao.get_all_users()
        logger.info("Returning %s users", len(users))
        return users
