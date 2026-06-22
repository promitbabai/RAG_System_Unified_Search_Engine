import logging
from typing import List

from fastapi import APIRouter, Depends, Path, status

from app.dao.user_dao import UserDAO
from app.schemas.user_schema import ErrorResponse, UserResponse
from app.services.user_service import UserService

logger = logging.getLogger(__name__)

router = APIRouter()


def get_user_dao() -> UserDAO:
    return UserDAO()


def get_user_service(user_dao: UserDAO = Depends(get_user_dao)) -> UserService:
    return UserService(user_dao=user_dao)


@router.get(
    "/users",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Get list of users",
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
def get_users_list(user_service: UserService = Depends(get_user_service)):
    """Controller endpoint to retrieve the list of all users."""
    logger.info("Received request for all users")
    return user_service.get_all_users()


@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get user details by user ID",
    responses={
        404: {"model": ErrorResponse, "description": "User not found"},
        422: {"model": ErrorResponse, "description": "Invalid input"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
def get_user_by_id(
    user_id: int = Path(..., description="User ID", example=10001, gt=0),
    user_service: UserService = Depends(get_user_service),
):
    """Controller endpoint to retrieve user details for a given user ID."""
    logger.info("Received request for user_id=%s", user_id)
    return user_service.get_user_details(user_id)
