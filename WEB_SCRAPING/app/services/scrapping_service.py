import requests
from fastapi import HTTPException
from pydantic import HttpUrl
from bs4 import BeautifulSoup


def scrape_webpage(userUrl: str):
    # This is your service layer
    print(f"Received URL in service layer: {userUrl}")  # ✅ prints in console
    response = requests.get(str(userUrl), timeout=10)

    if response.status_code != 200:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to fetch URL. Status: {response.status_code}"
        )

    html_content = response.text  # raw HTML 【3-06fea7】

    # Step 2: Parse HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Step 3: Extract readable text
    text = soup.get_text(separator="\n", strip=True)

    return {
        "url": userUrl,
        "content": text[:5000]  # limit output (avoid huge response)
    }

    # you can also modify / process the URL if neededpip l
    return {
        "message": f"Processed URL in service layer",
        "url": userUrl
    }



