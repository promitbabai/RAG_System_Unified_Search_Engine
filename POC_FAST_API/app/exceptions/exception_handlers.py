import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.exceptions.custom_exceptions import (
    UserNotFoundException,
    InvalidWikipediaURLException,
    WikipediaScrapingException,
)

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """Register application-level exception handlers."""

    @app.exception_handler(UserNotFoundException)
    async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
        logger.warning("Handled UserNotFoundException: %s", exc.message)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error_code": "USER_NOT_FOUND",
                "message": exc.message,
            },
        )

    @app.exception_handler(InvalidWikipediaURLException)
    async def invalid_wikipedia_url_exception_handler(request: Request, exc: InvalidWikipediaURLException):
        logger.warning("Handled InvalidWikipediaURLException: %s", exc.message)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error_code": "INVALID_WIKIPEDIA_URL",
                "message": exc.message,
            },
        )

    @app.exception_handler(WikipediaScrapingException)
    async def wikipedia_scraping_exception_handler(request: Request, exc: WikipediaScrapingException):
        logger.warning("Handled WikipediaScrapingException: %s", exc.message)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error_code": "WIKIPEDIA_SCRAPING_ERROR",
                "message": exc.message,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning("Validation error for request %s: %s", request.url.path, exc.errors())
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error_code": "VALIDATION_ERROR",
                "message": "Invalid request input",
                "details": exc.errors(),
            },
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled exception for request %s", request.url.path)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error_code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
            },
        )
