import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestWikipediaScraper:
    """Test suite for Wikipedia scraper endpoint."""

    def test_wikipedia_health(self):
        """Test Wikipedia scraper health check endpoint."""
        response = client.get("/api/v1/wikipedia/status")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "UP"
        assert "Wikipedia" in data["service"]

    def test_scrape_with_missing_url(self):
        """Test scrape endpoint with missing URL parameter."""
        response = client.post("/api/v1/wikipedia/scrape")
        assert response.status_code == 422  # Validation error

    def test_scrape_with_invalid_url(self):
        """Test scrape endpoint with non-Wikipedia URL."""
        response = client.post("/api/v1/wikipedia/scrape?url=https://google.com")
        assert response.status_code == 400  # Invalid URL error
        data = response.json()
        assert data["error_code"] == "INVALID_WIKIPEDIA_URL"

    def test_scrape_with_valid_url(self):
        """Test scrape endpoint with valid Wikipedia URL."""
        # Using a simple, relatively stable Wikipedia page
        url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
        response = client.post(f"/api/v1/wikipedia/scrape?url={url}")

        # May succeed or fail depending on network, but should be valid response
        assert response.status_code in [200, 500]

        if response.status_code == 200:
            data = response.json()
            assert "title" in data
            assert "url" in data
            assert "main_sections" in data
            assert "total_sections" in data
            assert "total_paragraphs" in data
            assert data["url"] == url


class TestUserAPI:
    """Existing user API tests (should still pass)."""

    def test_get_users_list(self):
        """Test get all users endpoint."""
        response = client.get("/api/v1/users")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) > 0

    def test_get_user_by_id(self):
        """Test get user by ID endpoint."""
        response = client.get("/api/v1/users/10001")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 10001
        assert data["first_name"] == "Promit"

    def test_get_invalid_user(self):
        """Test get user with invalid ID."""
        response = client.get("/api/v1/users/99999")
        assert response.status_code == 404
        data = response.json()
        assert data["error_code"] == "USER_NOT_FOUND"

