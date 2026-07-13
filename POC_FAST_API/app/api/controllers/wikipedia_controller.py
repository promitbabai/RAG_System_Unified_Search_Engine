import logging

from fastapi import APIRouter, Query, status

from app.schemas.wikipedia_schema import (
    WikipediaContentResponse,
    ErrorResponse,
    WikipediaMainSectionSchema,
    WikipediaSectionSchema,
    WikipediaParagraphSchema,
)
from app.services.wikipedia_service import WikipediaScraperService
from app.models.wikipedia import WikipediaContent

logger = logging.getLogger(__name__)

router = APIRouter()
scraper_service = WikipediaScraperService()


def _format_response(content: WikipediaContent) -> WikipediaContentResponse:
    """Convert WikipediaContent model to API response schema."""
    main_sections = []

    for section in content.main_sections:
        paragraphs = [
            WikipediaParagraphSchema(content=p.content)
            for p in section.paragraphs
        ]

        subsections = []
        for subsec in section.subsections:
            subsec_paragraphs = [
                WikipediaParagraphSchema(content=p.content)
                for p in subsec.paragraphs
            ]
            subsections.append(
                WikipediaSectionSchema(
                    heading=subsec.heading,
                    paragraph_count=len(subsec_paragraphs),
                    paragraphs=subsec_paragraphs,
                )
            )

        main_sections.append(
            WikipediaMainSectionSchema(
                heading=section.heading,
                paragraph_count=len(paragraphs),
                paragraphs=paragraphs,
                subsection_count=len(subsections),
                subsections=subsections,
            )
        )

    total_paragraphs = sum(
        len(s.paragraphs) + sum(len(ss.paragraphs) for ss in s.subsections)
        for s in content.main_sections
    )

    return WikipediaContentResponse(
        title=content.title,
        url=content.url,
        total_sections=len(main_sections),
        total_paragraphs=total_paragraphs,
        main_sections=main_sections,
    )


@router.post(
    "/scrape",
    response_model=WikipediaContentResponse,
    status_code=status.HTTP_200_OK,
    summary="Scrape Wikipedia Page",
    responses={
        400: {"model": ErrorResponse, "description": "Invalid Wikipedia URL"},
        422: {"model": ErrorResponse, "description": "Invalid input"},
        500: {"model": ErrorResponse, "description": "Scraping error"},
    },
)
def scrape_wikipedia(
    url: str = Query(
        ...,
        description="Wikipedia URL to scrape",
        example="https://en.wikipedia.org/wiki/Python_(programming_language)",
    )
):
    """
    Scrape a Wikipedia page and return hierarchically organized content.

    This endpoint:
    - Accepts a Wikipedia URL
    - Extracts title, headings (H1, H2), and paragraphs
    - Organizes content hierarchically (H1 → H2 → Paragraphs)
    - Prints formatted output to console logs
    - Returns structured JSON response

    **Example Usage:**
    ```
    POST /api/v1/wikipedia/scrape?url=https://en.wikipedia.org/wiki/FastAPI
    ```
    """
    logger.info("Received Wikipedia scraping request for URL: %s", url)

    # Scrape and get content
    content = scraper_service.scrape_wikipedia(url)

    # Format response
    response = _format_response(content)

    logger.info(
        "Successfully processed Wikipedia scrape: %s with %d sections",
        response.title,
        response.total_sections,
    )

    return response


@router.get(
    "/status",
    status_code=status.HTTP_200_OK,
    summary="Wikipedia Scraper Health Check",
)
def wikipedia_health():
    """Health check endpoint for Wikipedia scraper service."""
    logger.debug("Wikipedia scraper health check")
    return {
        "status": "UP",
        "service": "Wikipedia Scraper",
        "description": "Production-grade Wikipedia content scraper with hierarchical organization",
    }

