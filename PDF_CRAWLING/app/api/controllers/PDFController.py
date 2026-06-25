import logging

from fastapi import APIRouter
from starlette import status

from app.model.response_model import PDFAcceptModel, ErrorResponse

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/pdf-crawling",
    response_model=PDFAcceptModel,
    status_code=status.HTTP_200_OK,
    summary="Get list of users",
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
def process_pdf():
    """Controller endpoint to retrieve the list of all users."""
    logger.info("Receive the PDF file to process")
    model = PDFAcceptModel(status = "Accepted", message="Processing")
    return model