from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration.

    Values can be overridden using environment variables.
    Example:
        APP_NAME="User Service API"
        LOG_LEVEL="DEBUG"
    """

    APP_NAME: str = "User Service API"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    LOG_LEVEL: str = "INFO"


settings = Settings()
