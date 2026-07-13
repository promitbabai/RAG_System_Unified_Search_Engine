from pydantic import BaseModel, Field
from typing import List


class WikipediaParagraph(BaseModel):
    """Represents a paragraph of text from Wikipedia."""

    content: str = Field(..., description="The paragraph text content")


class WikipediaSection(BaseModel):
    """Represents a section with H2 heading and its paragraphs."""

    heading: str = Field(..., description="H2 heading text")
    paragraphs: List[WikipediaParagraph] = Field(
        default_factory=list, description="List of paragraphs in this section"
    )


class WikipediaMainSection(BaseModel):
    """Represents a main H1 section with subsections and content."""

    heading: str = Field(..., description="H1 heading or section title")
    paragraphs: List[WikipediaParagraph] = Field(
        default_factory=list, description="Paragraphs directly under this H1"
    )
    subsections: List[WikipediaSection] = Field(
        default_factory=list, description="H2 subsections with their content"
    )


class WikipediaContent(BaseModel):
    """Complete hierarchical Wikipedia page content."""

    title: str = Field(..., description="Page title")
    url: str = Field(..., description="Wikipedia URL")
    main_sections: List[WikipediaMainSection] = Field(
        default_factory=list, description="Main H1 sections of the page"
    )

