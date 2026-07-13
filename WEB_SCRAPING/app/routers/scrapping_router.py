from fastapi import APIRouter
from pydantic import HttpUrl, BaseModel
from app.services.scrapping_service import scrape_webpage

#class URLRequest(BaseModel):
#    url: HttpUrl

router = APIRouter(
    prefix="/scrapper",        # base URL path
    tags=["Scrapper"]          # for Swagger docs
)


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
