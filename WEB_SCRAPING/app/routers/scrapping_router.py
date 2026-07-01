from fastapi import APIRouter
from pydantic import HttpUrl, BaseModel
from app.services.scrapping_service import scrape_webpage

#class URLRequest(BaseModel):
#    url: HttpUrl

router = APIRouter(
    prefix="/scrapper",        # base URL path
    tags=["Scrapper"]          # for Swagger docs
)

# http://127.0.0.1:8000/scrapper/?url=https://www.incometax.gov.in/iec/foportal/   (WORKING)
# http://127.0.0.1:8000/scrapper/?url=https://rickcarlino.medium.com/fabulous-text-only-websites-cb17012d2d24
# https://www.wikipedia.org/
# https://www.incometax.gov.in/iec/foportal/
# https://uidai.gov.in/en/
# http://localhost:8000
# http://127.0.0.1:8000/scrapper/?url=https://sports.ndtv.com/fifa-world-cup-2026/michael-olise-the-bayern-munich-hero-driving-frances-dream-of-world-cup-glory-11710908?pfrom=home-ndtv_fifa


@router.get("/")
def scrape_html(url: str):
    # ✅ Pass URL to service layer
    return scrape_webpage(url)







#--------------------------------------------------------------
# send the URL in REQUEST BODY

#class WebsiteRequest(BaseModel):
#    url: str

#@router.post("/")
#def handle_website(request: WebsiteRequest):
#    return process_website_url(request.url)
