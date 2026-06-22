from fastapi import FastAPI

from app.api.controllers.user_controller import router as user_router
from app.core.config import settings
from app.core.logging_config import configure_logging
from app.exceptions.exception_handlers import register_exception_handlers


def create_app() -> FastAPI:
    """Application factory for creating the FastAPI app instance."""
    configure_logging()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Production-ready FastAPI sample with Controller, Service, DAO, Models, Exception Handling, and Logging.",
    )

    register_exception_handlers(app)

    app.include_router(user_router, prefix=settings.API_PREFIX, tags=["Users"])

    @app.get("/health", tags=["Health"])
    def health_check():
        return {"status": "UP", "application": settings.APP_NAME, "version": settings.APP_VERSION}

    return app


app = create_app()
