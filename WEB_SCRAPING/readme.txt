
WEBSCRAPING+CHROMADB (Both Running as CONTAINERS)
docker-compose up --build -d
docker-compose down --remove-orphans


Web Scraping running at = http://localhost:8001/
ChromaDB running at = http://localhost:8000/

# Scrape a webpage
curl "http://localhost:8001/scrapper/?url=https://www.incometax.gov.in/iec/foportal/"

# Scrape & store in Chroma
curl "http://localhost:8001/scrapenhance/?url=https://www.incometax.gov.in/iec/foportal/&store=true"

# Search Chroma
curl "http://localhost:8001/scrapenhance/search?query=income"
curl "http://localhost:8001/scrapenhance/search?query=deductions on which I can get tax benefit"

# Get stats
curl http://localhost:8001/scrapenhance/stats


WORKING FINE URL
------------------------

http://localhost:8001/scrapenhance/?url=https://www.incometax.gov.in/iec/foportal/&store=true


scrapping_router_enhanced.py
    => scrape_html()
          scrape_router.scrape_webpage()
              =>   # Step 2: Parse HTML

    => chroma_service.store_content()





url = http://localhost:8001/scrapenhance/stats   (working fine)
BROWSER RESPONSE = {
  "collection_name": "web-scraping",
  "document_count": 1,
  "status": "healthy"
}


SOME GOOD PAGES TO SCRAPE
-----------------------------
http://localhost:8001/scrapper/?url=https://www.edelweisslife.in/blogs/tax-filing/6-important-income-tax-rules
