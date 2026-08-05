import logging

from fastapi import APIRouter, Depends, Path, status
from app.dao import query_chroma

from app.schemas.user_schema import ErrorResponse

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get(
    "/query"
    "",
    response_model=str,
    status_code=status.HTTP_200_OK,
    summary="Get list of users",
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
def get_query():
    """Controller endpoint to retrieve the list of all users."""
    logger.info("Received request for all users")
    return query_chroma.query()