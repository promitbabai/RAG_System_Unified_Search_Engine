import uuid

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration.

    Values can be overridden using environment variables.
    Example:
        APP_NAME="User Service API"
        LOG_LEVEL="DEBUG"
    """

    APP_NAME: str = "PDF_Crawling"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = "/pdf/api/v1"
    LOG_LEVEL: str = "INFO"
    SERVICE_ID: str = f"{APP_NAME}-{uuid.uuid4()}"


settings = Settings()
