import asyncio
from crawl4ai import AsyncWebCrawler
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat

async def crawl(url):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url)

        return {
            "url": url,
            "markdown": result.markdown
        }

data = asyncio.run(
    crawl("https://en.wikipedia.org/wiki/2023_Cricket_World_Cup")
)
print(data["markdown"][:1000])
converter = DocumentConverter()

result = converter.convert_string(
    content=data["markdown"],
    format=InputFormat.MD
)

doc = result.document
