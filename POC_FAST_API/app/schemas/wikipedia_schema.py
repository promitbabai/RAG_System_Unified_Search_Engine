from pydantic import BaseModel, Field
from typing import List


class WikipediaParagraphSchema(BaseModel):
    """API response schema for a paragraph."""

    content: str = Field(..., description="Paragraph text content")


class WikipediaSectionSchema(BaseModel):
    """API response schema for a section with H2 heading."""

    heading: str = Field(..., description="H2 section heading")
    paragraph_count: int = Field(
        ..., description="Number of paragraphs in this section"
    )
    paragraphs: List[WikipediaParagraphSchema] = Field(
        default_factory=list, description="Paragraphs in this section"
    )


class WikipediaMainSectionSchema(BaseModel):
    """API response schema for a main H1 section."""

    heading: str = Field(..., description="H1 section heading")
    paragraph_count: int = Field(
        ..., description="Number of paragraphs under this H1"
    )
    paragraphs: List[WikipediaParagraphSchema] = Field(
        default_factory=list, description="Paragraphs directly under this H1"
    )
    subsection_count: int = Field(
        ..., description="Number of H2 subsections"
    )
    subsections: List[WikipediaSectionSchema] = Field(
        default_factory=list, description="H2 subsections"
    )


class WikipediaContentResponse(BaseModel):
    """API response schema for Wikipedia page content."""

    title: str = Field(..., description="Wikipedia page title")
    url: str = Field(..., description="Source Wikipedia URL")
    total_sections: int = Field(..., description="Total number of main H1 sections")
    total_paragraphs: int = Field(
        ..., description="Total number of paragraphs across all sections"
    )
    main_sections: List[WikipediaMainSectionSchema] = Field(
        default_factory=list, description="Hierarchical page content"
    )


class ErrorResponse(BaseModel):
    """Standard API error response schema."""

    error_code: str = Field(..., description="Error code identifier")
    message: str = Field(..., description="Error message")

