#!/usr/bin/env python3
"""
Example usage script for Wikipedia Scraper.

This script demonstrates how to use the Wikipedia scraper
both directly and through the FastAPI endpoints.

Usage:
    python examples/wiki_scraper_example.py
"""

import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.wikipedia_service import WikipediaScraperService


def example_1_direct_service_usage():
    """Example 1: Using the scraper service directly."""
    print("\n" + "="*80)
    print("EXAMPLE 1: Direct Service Usage")
    print("="*80 + "\n")

    service = WikipediaScraperService()

    # Scrape Python Wikipedia page
    url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    print(f"Scraping: {url}\n")

    try:
        content = service.scrape_wikipedia(url)

        # Display results
        print(f"\n📄 Title: {content.title}")
        print(f"📍 URL: {content.url}")
        print(f"📊 Total Sections: {len(content.main_sections)}")

        # Show first section details
        if content.main_sections:
            first_section = content.main_sections[0]
            print(f"\n🔍 First Section: {first_section.heading}")
            print(f"   Direct Paragraphs: {len(first_section.paragraphs)}")
            print(f"   Subsections: {len(first_section.subsections)}")

            if first_section.paragraphs:
                first_para = first_section.paragraphs[0].content[:150]
                print(f"   First Paragraph: {first_para}...")

    except Exception as e:
        print(f"❌ Error: {e}")


def example_2_api_endpoint_simulation():
    """Example 2: Simulating API usage with requests."""
    print("\n" + "="*80)
    print("EXAMPLE 2: API Endpoint Simulation")
    print("="*80 + "\n")

    print("To use this example, start the FastAPI server first:")
    print("  uvicorn app.main:app --reload\n")

    print("Then use curl or Python requests:")
    print("\nUsing curl:")
    print("""
    curl -X POST "http://localhost:8000/api/v1/wikipedia/scrape?url=https://en.wikipedia.org/wiki/FastAPI"
    """)

    print("Using Python requests:")
    print("""
    import requests
    
    url = "https://en.wikipedia.org/wiki/FastAPI"
    response = requests.post(
        "http://localhost:8000/api/v1/wikipedia/scrape",
        params={"url": url}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"Title: {data['title']}")
        print(f"Sections: {data['total_sections']}")
    else:
        print(f"Error: {response.json()}")
    """)


def example_3_hierarchical_processing():
    """Example 3: Processing hierarchical content."""
    print("\n" + "="*80)
    print("EXAMPLE 3: Hierarchical Content Processing")
    print("="*80 + "\n")

    service = WikipediaScraperService()
    url = "https://en.wikipedia.org/wiki/Machine_learning"

    print(f"Scraping: {url}\n")

    try:
        content = service.scrape_wikipedia(url)

        print("\n📚 HIERARCHICAL STRUCTURE:\n")

        for i, section in enumerate(content.main_sections[:3], 1):  # First 3 sections
            print(f"📌 Section {i}: {section.heading}")
            print(f"   └─ Paragraphs: {len(section.paragraphs)}")

            # Show first paragraph
            if section.paragraphs:
                first_para = section.paragraphs[0].content[:100]
                print(f"   └─ Content: {first_para}...")

            # Show subsections
            if section.subsections:
                print(f"   └─ Subsections: {len(section.subsections)}")
                for j, subsec in enumerate(section.subsections[:2], 1):  # First 2 subsections
                    print(f"      {j}. {subsec.heading}")
                    print(f"         └─ Paragraphs: {len(subsec.paragraphs)}")

            print()

    except Exception as e:
        print(f"❌ Error: {e}")


def example_4_error_handling():
    """Example 4: Error handling demonstration."""
    print("\n" + "="*80)
    print("EXAMPLE 4: Error Handling")
    print("="*80 + "\n")

    service = WikipediaScraperService()

    # Test 1: Invalid URL (not Wikipedia)
    print("Test 1: Invalid URL (non-Wikipedia)")
    try:
        service.scrape_wikipedia("https://google.com")
    except Exception as e:
        print(f"✓ Caught exception: {type(e).__name__}")
        print(f"  Message: {e}\n")

    # Test 2: Invalid URL format
    print("Test 2: Invalid URL format")
    try:
        service.scrape_wikipedia("not a url")
    except Exception as e:
        print(f"✓ Caught exception: {type(e).__name__}")
        print(f"  Message: {e}\n")

    # Test 3: Non-existent Wikipedia page (would get a different page or error)
    print("Test 3: Valid format but might fail (network-dependent)")
    try:
        service.scrape_wikipedia("https://en.wikipedia.org/wiki/Nonexistent_Article_XYZ_12345")
        print("✓ Request succeeded (Wikipedia might redirect or return article)\n")
    except Exception as e:
        print(f"✓ Caught exception: {type(e).__name__}")
        print(f"  Message: {e}\n")


def example_5_json_export():
    """Example 5: Exporting to JSON."""
    print("\n" + "="*80)
    print("EXAMPLE 5: JSON Export")
    print("="*80 + "\n")

    service = WikipediaScraperService()
    url = "https://en.wikipedia.org/wiki/FastAPI"

    print(f"Scraping: {url}\n")

    try:
        content = service.scrape_wikipedia(url)

        # Convert to JSON (using Pydantic's model_dump)
        json_data = json.loads(content.model_dump_json(indent=2))

        print("\n📄 JSON STRUCTURE (first section only):\n")
        if json_data["main_sections"]:
            first_section = json_data["main_sections"][0]
            print(json.dumps(first_section, indent=2)[:500] + "\n...\n")

        # Save to file
        output_file = "wikipedia_scrape_result.json"
        with open(output_file, "w") as f:
            json.dump(json_data, f, indent=2)

        print(f"✓ Full JSON saved to: {output_file}")

    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Run all examples."""
    print("\n" + "="*80)
    print("WIKIPEDIA SCRAPER EXAMPLES")
    print("="*80)

    print("\nNote: Examples 1, 3, 4, and 5 require internet connection")
    print("and may take a few seconds to complete.\n")

    try:
        # Example 1: Direct service usage
        example_1_direct_service_usage()

        # Example 2: API endpoint simulation
        example_2_api_endpoint_simulation()

        # Example 3: Hierarchical processing
        example_3_hierarchical_processing()

        # Example 4: Error handling
        example_4_error_handling()

        # Example 5: JSON export
        example_5_json_export()

        print("\n" + "="*80)
        print("✅ ALL EXAMPLES COMPLETED")
        print("="*80 + "\n")

    except KeyboardInterrupt:
        print("\n\n⏹️  Examples interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

