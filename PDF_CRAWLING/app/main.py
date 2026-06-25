from fastapi import FastAPI

from app.api.controllers.PDFController import router as pdf_router
from app.core.config import settings
from app.core.logging_config import configure_logging
from app.exceptions.exception_handlers import register_exception_handlers
from app.service.service_registery import lifespan


def create_app() -> FastAPI:
    """Application factory for creating the FastAPI app instance."""
    configure_logging()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Upload the PDF and crawling for Data Embedding",
        lifespan=lifespan
    )

    register_exception_handlers(app)

    app.include_router(pdf_router, prefix=settings.API_PREFIX, tags=["PDF"])

    @app.get("/health", tags=["Health"])
    def health_check():
        return {"status": "UP", "application": settings.APP_NAME, "version": settings.APP_VERSION}

    return app


app = create_app()
