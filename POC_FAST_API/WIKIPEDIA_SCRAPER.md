# Wikipedia Scraper Module

A production-grade Wikipedia scraper built with FastAPI that extracts and organizes content hierarchically.

## Features

✅ **Accepts Wikipedia URLs** - Validates and processes Wikipedia URLs  
✅ **Extracts Structured Content** - Title, headings (H1, H2), and paragraphs  
✅ **Hierarchical Organization** - H1 → H2 → Paragraphs structure  
✅ **Console Logging** - Formatted output with all scraped content  
✅ **JSON Response** - Structured API response with complete metadata  
✅ **Production Architecture** - Controller → Service pattern with proper error handling  

## Architecture

The Wikipedia scraper follows a clean, layered architecture:

```
Wikipedia Feature Structure:
├── Models (app/models/wikipedia.py)
│   ├── WikipediaParagraph
│   ├── WikipediaSection
│   ├── WikipediaMainSection
│   └── WikipediaContent
├── Schemas (app/schemas/wikipedia_schema.py)
│   ├── WikipediaParagraphSchema
│   ├── WikipediaSectionSchema
│   ├── WikipediaMainSectionSchema
│   └── WikipediaContentResponse
├── Service (app/services/wikipedia_service.py)
│   └── WikipediaScraperService
│       ├── scrape_wikipedia()
│       ├── _validate_wikipedia_url()
│       ├── _extract_title()
│       ├── _extract_sections()
│       └── _print_to_console()
├── Controller (app/api/controllers/wikipedia_controller.py)
│   └── Router with endpoints:
│       ├── POST /scrape
│       └── GET /status
└── Exceptions (app/exceptions/custom_exceptions.py)
    ├── InvalidWikipediaURLException
    └── WikipediaScrapingException
```

## API Endpoints

### 1. Scrape Wikipedia Page

**Endpoint:** `POST /api/v1/wikipedia/scrape`

**Query Parameters:**
- `url` (required): Wikipedia URL to scrape

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/wikipedia/scrape?url=https://en.wikipedia.org/wiki/Python_(programming_language)"
```

**Request with Python:**
```python
import requests

url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
response = requests.post(
    "http://localhost:8000/api/v1/wikipedia/scrape",
    params={"url": url}
)
data = response.json()
print(data)
```

**Response (Success - 200 OK):**
```json
{
  "title": "Python (programming language)",
  "url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
  "total_sections": 15,
  "total_paragraphs": 145,
  "main_sections": [
    {
      "heading": "History",
      "paragraph_count": 5,
      "paragraphs": [
        {
          "content": "Python is a high-level, general-purpose programming language..."
        }
      ],
      "subsection_count": 2,
      "subsections": [
        {
          "heading": "Design philosophy and features",
          "paragraph_count": 3,
          "paragraphs": [...]
        }
      ]
    }
  ]
}
```

**Response (Invalid URL - 400 Bad Request):**
```json
{
  "error_code": "INVALID_WIKIPEDIA_URL",
  "message": "Invalid Wikipedia URL 'https://google.com': URL is not a Wikipedia URL"
}
```

**Response (Scraping Error - 500 Internal Server Error):**
```json
{
  "error_code": "WIKIPEDIA_SCRAPING_ERROR",
  "message": "Failed to scrape Wikipedia URL 'https://...': Failed to fetch URL: <reason>"
}
```

### 2. Health Check

**Endpoint:** `GET /api/v1/wikipedia/status`

**Example Request:**
```bash
curl http://localhost:8000/api/v1/wikipedia/status
```

**Response:**
```json
{
  "status": "UP",
  "service": "Wikipedia Scraper",
  "description": "Production-grade Wikipedia content scraper with hierarchical organization"
}
```

## Console Output

The service automatically prints formatted output to the console logger:

```
================================================================================
WIKIPEDIA SCRAPE RESULT
================================================================================
Title: Python (programming language)
URL: https://en.wikipedia.org/wiki/Python_(programming_language)
Total Sections: 15
================================================================================
[Section 1] History
  Direct Paragraphs: 5
  • Python is a high-level, general-purpose programming language...
  Subsections: 2
    [1.1] Design philosophy and features
      Paragraphs: 3
      • The core philosophy of Python is summarized in the document "The Zen...
    [1.2] Uses
      Paragraphs: 2
      • Python is widely used in various fields...
[Section 2] Syntax and semantics
  ...
================================================================================
```

## Usage Examples

### Example 1: Basic Python Usage

```python
from app.services.wikipedia_service import WikipediaScraperService

service = WikipediaScraperService()

url = "https://en.wikipedia.org/wiki/FastAPI"
content = service.scrape_wikipedia(url)

print(f"Title: {content.title}")
print(f"Sections: {len(content.main_sections)}")

for section in content.main_sections:
    print(f"\n## {section.heading}")
    for para in section.paragraphs[:1]:  # First paragraph
        print(f"   {para.content[:100]}...")
```

### Example 2: Complete API Request with Response Processing

```python
import requests
import json

def scrape_and_process(wikipedia_url):
    """Scrape Wikipedia and process hierarchical content."""
    
    response = requests.post(
        "http://localhost:8000/api/v1/wikipedia/scrape",
        params={"url": wikipedia_url}
    )
    
    if response.status_code != 200:
        print(f"Error: {response.json()}")
        return
    
    data = response.json()
    
    # Display summary
    print(f"📄 {data['title']}")
    print(f"📍 URL: {data['url']}")
    print(f"📊 Sections: {data['total_sections']}, Paragraphs: {data['total_paragraphs']}")
    print("\n" + "="*60 + "\n")
    
    # Display hierarchical content
    for section in data['main_sections']:
        print(f"# {section['heading']}")
        print(f"  Paragraphs: {section['paragraph_count']}")
        
        if section['subsections']:
            print(f"  Subsections: {section['subsection_count']}")
            for subsec in section['subsections']:
                print(f"  ## {subsec['heading']}")
                print(f"     Paragraphs: {subsec['paragraph_count']}")
        
        print()

# Usage
scrape_and_process("https://en.wikipedia.org/wiki/Machine_Learning")
```

### Example 3: Using FastAPI TestClient

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Test scraping
response = client.post(
    "/api/v1/wikipedia/scrape",
    params={"url": "https://en.wikipedia.org/wiki/Artificial_intelligence"}
)

if response.status_code == 200:
    content = response.json()
    print(f"Successfully scraped: {content['title']}")
    print(f"Total paragraphs extracted: {content['total_paragraphs']}")
else:
    print(f"Error: {response.json()}")
```

## Error Handling

The scraper includes comprehensive error handling:

| Status Code | Error Code | Reason |
|---|---|---|
| 400 | `INVALID_WIKIPEDIA_URL` | URL is not a valid Wikipedia URL |
| 422 | `VALIDATION_ERROR` | Missing required `url` parameter |
| 500 | `WIKIPEDIA_SCRAPING_ERROR` | Failed to fetch or parse Wikipedia page |
| 500 | `INTERNAL_SERVER_ERROR` | Unexpected server error |

## Dependencies

- **requests** - HTTP client for fetching Wikipedia pages
- **beautifulsoup4** - HTML parsing and content extraction
- **fastapi** - Web framework
- **pydantic** - Data validation and serialization

## Environment Configuration

The scraper respects application-level settings from `app/core/config.py`:

```python
class Settings(BaseSettings):
    APP_NAME: str = "User Service API"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    LOG_LEVEL: str = "INFO"  # Change to DEBUG for detailed logging
```

## Running the Application

### 1. Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Start the server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Access the API:
```
http://localhost:8000/docs  # Swagger UI
http://localhost:8000/redoc # ReDoc
```

## Testing

Run the test suite:

```bash
pytest tests/test_wikipedia_scraper.py -v
```

Test individual endpoints:

```bash
# Health check
pytest tests/test_wikipedia_scraper.py::TestWikipediaScraper::test_wikipedia_health -v

# Invalid URL
pytest tests/test_wikipedia_scraper.py::TestWikipediaScraper::test_scrape_with_invalid_url -v

# Missing URL
pytest tests/test_wikipedia_scraper.py::TestWikipediaScraper::test_scrape_with_missing_url -v
```

## Performance Considerations

1. **Caching** - Consider caching frequently scraped pages
2. **Rate Limiting** - Wikipedia may have rate limits for automated access
3. **Timeout** - Default timeout is 10 seconds per request
4. **Parsing** - BeautifulSoup parsing is done in-memory (suitable for typical Wikipedia pages)

## Limitations & Future Enhancements

- **Single Page Processing** - Currently processes one URL at a time
- **Language Support** - Works with any Wikipedia language version
- **Image Extraction** - Currently skips images (can be extended)
- **Table Extraction** - Could be enhanced to extract tables
- **Caching Layer** - Could add Redis caching for frequently accessed pages
- **Async Support** - Could be converted to async for better concurrency
- **Batch Processing** - Could support scraping multiple URLs

## Production Checklist

- ✅ Proper error handling and custom exceptions
- ✅ Comprehensive logging
- ✅ Input validation
- ✅ Clean architecture (Controller → Service pattern)
- ✅ Type hints for all functions
- ✅ Docstrings for all public methods
- ✅ Unit tests included
- ✅ OpenAPI documentation
- ✅ Hierarchical data organization
- ✅ Console output for debugging

