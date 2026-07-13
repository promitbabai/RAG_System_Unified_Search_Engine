import logging
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from app.models.wikipedia import (
    WikipediaContent,
    WikipediaMainSection,
    WikipediaParagraph,
    WikipediaSection,
)
from app.exceptions.custom_exceptions import InvalidWikipediaURLException, WikipediaScrapingException

logger = logging.getLogger(__name__)


class WikipediaScraperService:
    """Service layer for Wikipedia scraping and content extraction."""

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def scrape_wikipedia(self, url: str) -> WikipediaContent:
        """
        Scrape a Wikipedia page and extract structured content hierarchically.

        Args:
            url: Wikipedia URL to scrape

        Returns:
            WikipediaContent: Hierarchically organized page content

        Raises:
            InvalidWikipediaURLException: If URL is not a valid Wikipedia URL
            WikipediaScrapingException: If scraping fails
        """
        logger.info("Starting Wikipedia scrape for URL: %s", url)

        # Validate URL
        self._validate_wikipedia_url(url)

        try:
            # Fetch page
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract title
            title = self._extract_title(soup)
            logger.info("Extracted title: %s", title)

            # Extract hierarchical content
            main_sections = self._extract_sections(soup)
            logger.info("Extracted %d main sections", len(main_sections))

            # Create WikipediaContent
            content = WikipediaContent(
                title=title,
                url=url,
                main_sections=main_sections
            )

            # Log to console
            self._print_to_console(content)

            logger.info("Successfully scraped Wikipedia page: %s", title)
            return content

        except requests.exceptions.RequestException as e:
            logger.error("Request error while scraping Wikipedia: %s", str(e))
            raise WikipediaScrapingException(
                url=url, reason=f"Failed to fetch URL: {str(e)}"
            )
        except Exception as e:
            logger.error("Unexpected error while scraping Wikipedia: %s", str(e))
            raise WikipediaScrapingException(
                url=url, reason=f"Scraping failed: {str(e)}"
            )

    def _validate_wikipedia_url(self, url: str) -> None:
        """Validate that URL is a Wikipedia URL."""
        logger.debug("Validating Wikipedia URL: %s", url)

        try:
            parsed = urlparse(url)
            if not parsed.netloc:
                raise ValueError("Invalid URL format")

            if "wikipedia.org" not in parsed.netloc:
                raise ValueError("URL is not a Wikipedia URL")

            logger.debug("URL validation passed")
        except ValueError as e:
            logger.warning("Invalid Wikipedia URL: %s", str(e))
            raise InvalidWikipediaURLException(url=url, reason=str(e))

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title from Wikipedia page."""
        logger.debug("Extracting page title")

        # Try to find the page title
        title_tag = soup.find("h1", class_="firstHeading")
        if title_tag:
            return title_tag.get_text().strip()

        # Fallback to page title from head
        title_tag = soup.find("title")
        if title_tag:
            text = title_tag.get_text().strip()
            # Remove " - Wikipedia" suffix if present
            if " - Wikipedia" in text:
                text = text.replace(" - Wikipedia", "").strip()
            return text

        return "Untitled"

    def _extract_sections(self, soup: BeautifulSoup) -> list[WikipediaMainSection]:
        """Extract hierarchical sections from page content."""
        logger.debug("Extracting page sections")

        main_sections = []
        current_h1 = None

        # Find the main content div
        content_div = soup.find("div", class_="mw-parser-output")
        if not content_div:
            logger.warning("Could not find main content div")
            return main_sections

        # Iterate through all elements
        for element in content_div.children:
            if isinstance(element, str):
                continue

            element_name = element.name

            # H2 heading - start of new main section
            if element_name == "h2":
                # Save previous section if exists
                if current_h1 is not None:
                    main_sections.append(current_h1)

                heading_text = self._extract_heading_text(element)
                current_h1 = WikipediaMainSection(
                    heading=heading_text,
                    paragraphs=[],
                    subsections=[]
                )
                logger.debug("Created new main section: %s", heading_text)

            # H3 heading - subsection (H2 in hierarchy)
            elif element_name == "h3" and current_h1 is not None:
                heading_text = self._extract_heading_text(element)
                subsection = WikipediaSection(
                    heading=heading_text,
                    paragraphs=[]
                )
                current_h1.subsections.append(subsection)
                logger.debug("Created new subsection: %s", heading_text)

            # Paragraph
            elif element_name == "p" and current_h1 is not None:
                text = self._extract_paragraph_text(element)
                if text.strip():
                    paragraph = WikipediaParagraph(content=text)

                    # Add to current subsection if exists, otherwise to main section
                    if current_h1.subsections:
                        current_h1.subsections[-1].paragraphs.append(paragraph)
                    else:
                        current_h1.paragraphs.append(paragraph)

        # Append last section
        if current_h1 is not None:
            main_sections.append(current_h1)

        logger.debug("Extracted %d main sections", len(main_sections))
        return main_sections

    def _extract_heading_text(self, heading_element) -> str:
        """Extract clean heading text from heading element."""
        # Remove edit links
        for edit_link in heading_element.find_all("span", class_="mw-editsection"):
            edit_link.decompose()

        text = heading_element.get_text().strip()
        return text

    def _extract_paragraph_text(self, paragraph_element) -> str:
        """Extract clean paragraph text from paragraph element."""
        # Remove reference links
        for ref in paragraph_element.find_all(["sup", "span"]):
            if ref.get("class"):
                classes = " ".join(ref.get("class", []))
                if "reference" in classes or "sorttext" in classes:
                    ref.decompose()

        text = paragraph_element.get_text().strip()
        # Clean up extra whitespace
        text = " ".join(text.split())
        return text

    def _print_to_console(self, content: WikipediaContent) -> None:
        """Print content to console in a formatted way."""
        logger.info("=" * 80)
        logger.info("WIKIPEDIA SCRAPE RESULT")
        logger.info("=" * 80)
        logger.info("Title: %s", content.title)
        logger.info("URL: %s", content.url)
        logger.info("Total Sections: %d", len(content.main_sections))
        logger.info("=" * 80)

        for i, section in enumerate(content.main_sections, 1):
            logger.info("[Section %d] %s", i, section.heading)
            logger.info("  Direct Paragraphs: %d", len(section.paragraphs))

            for para in section.paragraphs:
                logger.info("  • %s...", para.content[:100])

            if section.subsections:
                logger.info("  Subsections: %d", len(section.subsections))
                for j, subsec in enumerate(section.subsections, 1):
                    logger.info("    [%d.%d] %s", i, j, subsec.heading)
                    logger.info("      Paragraphs: %d", len(subsec.paragraphs))
                    for para in subsec.paragraphs:
                        logger.info("      • %s...", para.content[:80])

        logger.info("=" * 80)

