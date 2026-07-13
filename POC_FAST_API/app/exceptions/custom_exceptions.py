class UserNotFoundException(Exception):
    """Raised when the requested user is not found."""

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.message = f"User not found for user_id={user_id}"
        super().__init__(self.message)


class InvalidWikipediaURLException(Exception):
    """Raised when provided Wikipedia URL is invalid."""

    def __init__(self, url: str, reason: str):
        self.url = url
        self.reason = reason
        self.message = f"Invalid Wikipedia URL '{url}': {reason}"
        super().__init__(self.message)


class WikipediaScrapingException(Exception):
    """Raised when Wikipedia scraping fails."""

    def __init__(self, url: str, reason: str):
        self.url = url
        self.reason = reason
        self.message = f"Failed to scrape Wikipedia URL '{url}': {reason}"
        super().__init__(self.message)
