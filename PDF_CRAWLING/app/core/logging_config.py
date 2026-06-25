import logging
import sys

from app.core.config import settings


def configure_logging() -> None:
    """Configure application-wide logging."""
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
