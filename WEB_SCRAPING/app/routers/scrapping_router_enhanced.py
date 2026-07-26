from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from app.services.scrapping_service import scrape_webpage
from app.services.chroma_service import chroma_service

router = APIRouter(
    prefix="/scrapenhance",
    tags=["Scrapenhance"]
)
# http://127.0.0.1:8000/scrapenhance/?url=https://www.incometax.gov.in/iec/foportal/
# http://127.0.0.1:8000/scrapper/?url=https://www.incometax.gov.in/iec/foportal/   - SCRAPED SUCCESSFULLY
# http://127.0.0.1:8000/scrapper/?url=https://wb.gov.in/   - SCRAPED SUCCESSFULLY
# http://127.0.0.1:8000/scrapper/?url=https://www.india.gov.in/my-government/schemes - SCRAPED SUCCESSFULLY
# http://127.0.0.1:8000/scrapper/?url=https://rickcarlino.medium.com/fabulous-text-only-websites-cb17012d2d24 - SCRAPED SUCCESSFULLY
# http://127.0.0.1:8000/scrapper/?url=https://uidai.gov.in/en/about-uidai/legal-framework/rules.html
# https://www.wikipedia.org/
# https://www.incometax.gov.in/iec/foportal/
# https://uidai.gov.in/en/
# http://127.0.0.1:8000/scrapper/?url=https://www.tesco.com/?srsltid=AfmBOorQo-DKmXxr9ls-GVn5xlYjwdyLMG32RUtleI6kRi3AtRdItKeP
# http://localhost:8000
# http://127.0.0.1:8000/scrapper/?url=https://sports.ndtv.com/fifa-world-cup-2026/michael-olise-the-bayern-munich-hero-driving-frances-dream-of-world-cup-glory-11710908?pfrom=home-ndtv_fifa



class ScrapeAndStoreRequest(BaseModel):
    """Request model for scraping and storing in ChromaDB"""
    url: str
    store_in_chroma: bool = False  # Optional: store content in ChromaDB


@router.get("/")
def scrape_html(url: str, store: bool = False):
    """
    Scrape a webpage and optionally store in ChromaDB

    Args:
        url: The URL to scrape
        store: If True, store the content in ChromaDB
    """
    try:
        result = scrape_webpage(url)

        # Optionally store in ChromaDB
        if store:
            try:
                chroma_result = chroma_service.store_content(
                    url=url,
                    content=result.get("content", "")[:10000],  # Limit to 10k chars
                    metadata={"scraped_successfully": True}
                )
                result["chroma_stored"] = chroma_result
            except Exception as e:
                result["chroma_error"] = f"Failed to store in ChromaDB: {str(e)}"

        return result

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping error: {str(e)}")


@router.post("/scrape-and-store")
def scrape_and_store(request: ScrapeAndStoreRequest):
    """
    Scrape a webpage and store content in ChromaDB

    Args:
        request: ScrapeAndStoreRequest with URL and storage flag
    """
    try:
        # Scrape the webpage
        result = scrape_webpage(request.url)

        # Store in ChromaDB
        if request.store_in_chroma:
            chroma_result = chroma_service.store_content(
                url=request.url,
                content=result.get("content", "")[:10000],
                metadata={"source": "web_scraper"}
            )
            result["chroma_stored"] = chroma_result

        return result

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/search")
def search_chroma(query: str = Query(..., description="Search query")):
    """
    Search for similar content in ChromaDB

    Args:
        query: The search query
    """
    try:
        results = chroma_service.search_content(query, n_results=5)
        return {
            "query": query,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")


@router.get("/stats")
def get_stats():
    """Get ChromaDB collection statistics"""
    try:
        stats = chroma_service.get_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stats error: {str(e)}")


@router.delete("/clear-chroma")
def clear_chroma():
    """
    Delete all stored content in ChromaDB
    WARNING: This is destructive and cannot be undone
    """
    try:
        result = chroma_service.delete_collection()
        return {
            "status": "success",
            "message": "ChromaDB collection cleared",
            **result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

