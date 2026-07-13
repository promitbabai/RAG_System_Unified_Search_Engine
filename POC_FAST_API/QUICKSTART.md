# Wikipedia Scraper - Quick Start Guide

## Overview

This is a production-grade Wikipedia scraper built with FastAPI that extracts content hierarchically:
- **H1 headings** → Main sections
- **H2 headings** → Subsections  
- **Paragraphs** → Content organized under headings

## Installation

### 1. Install Dependencies

```bash
cd D:\projects\python\RAG_System_Unified_Search_Engine\POC_FAST_API
pip install -r requirements.txt
```

### 2. Start the FastAPI Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You'll see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## Quick Usage

### Option 1: Using Swagger UI (Browser)

1. Open: `http://localhost:8000/docs`
2. Find the **POST** `/api/v1/wikipedia/scrape` endpoint
3. Click **Try it out**
4. Enter a Wikipedia URL:
   ```
   https://en.wikipedia.org/wiki/FastAPI
   ```
5. Click **Execute**

### Option 2: Using cURL (Command Line)

```bash
curl -X POST "http://localhost:8000/api/v1/wikipedia/scrape?url=https://en.wikipedia.org/wiki/Python_(programming_language)"
```

### Option 3: Using Python

```python
import requests
import json

url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
response = requests.post(
    "http://localhost:8000/api/v1/wikipedia/scrape",
    params={"url": url}
)

if response.status_code == 200:
    data = response.json()
    print(f"📄 {data['title']}")
    print(f"📊 Sections: {data['total_sections']}")
    print(f"📝 Total Paragraphs: {data['total_paragraphs']}")
    
    # Show first section
    if data['main_sections']:
        section = data['main_sections'][0]
        print(f"\n## {section['heading']}")
        print(f"   Subsections: {section['subsection_count']}")
else:
    print(f"Error: {response.json()}")
```

## API Endpoints

### 1. Scrape Wikipedia

**POST** `/api/v1/wikipedia/scrape?url=<WIKIPEDIA_URL>`

**Parameters:**
- `url` (required): Full Wikipedia URL

**Response (Success):**
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
      "paragraphs": [...],
      "subsection_count": 2,
      "subsections": [...]
    }
  ]
}
```

### 2. Health Check

**GET** `/api/v1/wikipedia/status`

**Response:**
```json
{
  "status": "UP",
  "service": "Wikipedia Scraper",
  "description": "Production-grade Wikipedia content scraper with hierarchical organization"
}
```

## Example Wikipedia URLs to Try

```
https://en.wikipedia.org/wiki/Python_(programming_language)
https://en.wikipedia.org/wiki/FastAPI
https://en.wikipedia.org/wiki/Machine_learning
https://en.wikipedia.org/wiki/Artificial_intelligence
https://en.wikipedia.org/wiki/Docker_(software)
https://en.wikipedia.org/wiki/Kubernetes
https://en.wikipedia.org/wiki/Microservices
```

## Understanding the Output

### Console Output (Logs)

The scraper prints detailed output to console:

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
    [1.1] Early history (1989-1994)
      Paragraphs: 3
      • Python was conceived in December 1989...
    [1.2] Version 0.9.0 (February 1991)
      Paragraphs: 2
      • In February 1991, the first version...
[Section 2] Design philosophy and features
  Direct Paragraphs: 4
  Subsections: 1
    [2.1] Design philosophy
      Paragraphs: 2
      • Beautiful is better than ugly...
================================================================================
```

### JSON Response

The API returns a hierarchical JSON structure:

```json
{
  "main_sections": [
    {
      "heading": "History",
      "paragraph_count": 5,
      "paragraphs": [
        {"content": "Python is a high-level..."},
        {"content": "Guido van Rossum..."}
      ],
      "subsection_count": 2,
      "subsections": [
        {
          "heading": "Early history",
          "paragraph_count": 3,
          "paragraphs": [...]
        }
      ]
    }
  ]
}
```

## Error Handling

### Invalid URL

```bash
curl -X POST "http://localhost:8000/api/v1/wikipedia/scrape?url=https://google.com"
```

**Response (400 Bad Request):**
```json
{
  "error_code": "INVALID_WIKIPEDIA_URL",
  "message": "Invalid Wikipedia URL 'https://google.com': URL is not a Wikipedia URL"
}
```

### Missing URL Parameter

```bash
curl -X POST "http://localhost:8000/api/v1/wikipedia/scrape"
```

**Response (422 Unprocessable Entity):**
```json
{
  "error_code": "VALIDATION_ERROR",
  "message": "Invalid request input",
  "details": [...]
}
```

## Running Examples

```bash
# Run the example script
python examples/wiki_scraper_example.py
```

This runs 5 different examples showing:
1. Direct service usage
2. API endpoint simulation
3. Hierarchical processing
4. Error handling
5. JSON export

## Running Tests

```bash
# Run all tests
pytest tests/test_wikipedia_scraper.py -v

# Run specific test
pytest tests/test_wikipedia_scraper.py::TestWikipediaScraper::test_scrape_with_valid_url -v

# Run with coverage
pytest tests/test_wikipedia_scraper.py --cov=app --cov-report=html
```

## Project Structure

```
POC_FAST_API/
├── app/
│   ├── api/controllers/
│   │   ├── user_controller.py       # Existing user API
│   │   └── wikipedia_controller.py  # NEW: Wikipedia scraper API
│   ├── services/
│   │   ├── user_service.py
│   │   └── wikipedia_service.py     # NEW: Scraper logic
│   ├── models/
│   │   ├── user.py
│   │   └── wikipedia.py             # NEW: Data models
│   ├── schemas/
│   │   ├── user_schema.py
│   │   └── wikipedia_schema.py      # NEW: API response schemas
│   ├── exceptions/
│   │   ├── custom_exceptions.py     # UPDATED: Added Wikipedia exceptions
│   │   └── exception_handlers.py    # UPDATED: Added Wikipedia handlers
│   └── main.py                       # UPDATED: Registered Wikipedia router
├── tests/
│   ├── test_user_api.py
│   └── test_wikipedia_scraper.py    # NEW: Wikipedia tests
├── examples/
│   ├── __init__.py
│   └── wiki_scraper_example.py      # NEW: Usage examples
├── requirements.txt                  # UPDATED: Added beautifulsoup4, requests
├── WIKIPEDIA_SCRAPER.md             # NEW: Detailed documentation
└── QUICKSTART.md                    # NEW: This file
```

## Features Implemented ✅

✅ **Accepts Wikipedia URLs** - Full validation of Wikipedia URLs  
✅ **Scrapes Structured Content** - Extracts title, headings, paragraphs  
✅ **Hierarchical Organization** - H1 → H2 → Paragraphs structure  
✅ **Console Output** - Formatted logging of all scraped content  
✅ **JSON Response** - Complete API response with metadata  
✅ **Error Handling** - Custom exceptions for invalid URLs and scraping failures  
✅ **Production Architecture** - Clean controller → service pattern  
✅ **Type Hints** - Full type annotations  
✅ **Logging** - Comprehensive logging at all levels  
✅ **Tests** - Unit tests included  

## Troubleshooting

### Issue: Module not found errors

**Solution:** Make sure you're in the correct directory and have installed requirements:
```bash
cd D:\projects\python\RAG_System_Unified_Search_Engine\POC_FAST_API
pip install -r requirements.txt
```

### Issue: Connection refused errors

**Solution:** Make sure the FastAPI server is running:
```bash
uvicorn app.main:app --reload
```

### Issue: Wikipedia page not loading

**Solution:** Some Wikipedia pages may have anti-bot protections. Try:
1. Using a different Wikipedia URL
2. Adding a delay between requests
3. Checking your internet connection

### Issue: BeautifulSoup parsing issues

**Solution:** The parser might need different tags for certain Wikipedia pages. Check the console logs for details.

## Next Steps

1. ✅ Try scraping different Wikipedia pages
2. ✅ Examine the JSON response structure
3. ✅ Check the console logs for detailed output
4. ✅ Run the example script
5. ✅ Run the tests
6. ✅ Customize the scraper for your needs

## Documentation

- **Detailed Documentation:** See [WIKIPEDIA_SCRAPER.md](WIKIPEDIA_SCRAPER.md)
- **API Reference:** Visit `http://localhost:8000/docs` (Swagger UI)
- **Code Examples:** See [examples/wiki_scraper_example.py](examples/wiki_scraper_example.py)

## Support

For issues or questions:
1. Check the logs at the console
2. Review the error response JSON
3. Consult [WIKIPEDIA_SCRAPER.md](WIKIPEDIA_SCRAPER.md)
4. Run the test suite to verify setup

---

**Happy Scraping! 🚀**

