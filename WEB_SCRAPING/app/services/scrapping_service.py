import requests
from fastapi import HTTPException
from bs4 import BeautifulSoup
from app.services import chunking_service



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



def scrape_webpage(userUrl: str):
    # This is your service layer
    print(f"Received URL in service layer: {userUrl}")  # ✅ prints in console

    # Set up headers to mimic a real browser request
    # This prevents 400 Bad Request errors from sites with anti-bot protection
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

    try:
        response = requests.get(str(userUrl), timeout=10, headers=headers)

        if response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to fetch URL. Status: {response.status_code}"
            )

        html_content = response.text  # raw HTML

        # Step 2: Parse HTML
        soup = BeautifulSoup(html_content, "html.parser")

        # Step 3: Extract readable text
        text = soup.get_text(separator="\n", strip=True)

        # Step 4: call the Chunking service
        chunking_service.process_and_chunk_page(text)

        return {
            "url": userUrl,
            "content": text[:5000]  # limit output (avoid huge response)
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error fetching URL: {str(e)}"
        )



