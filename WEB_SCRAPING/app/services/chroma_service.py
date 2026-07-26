import os
import chromadb
from typing import List, Optional

# ChromaDB client initialization
# Use environment variable for Docker, fallback to localhost for local development
chroma_url = os.getenv("CHROMA_DB_URL", "http://localhost:8000")
host = chroma_url.replace("http://", "").replace("https://", "").split(":")[0]
port = int(chroma_url.split(":")[-1]) if ":" in chroma_url else 8000

print(f"Connecting to ChromaDB at {host}:{port}")
client = chromadb.HttpClient(host=host, port=port)


class ChromaDBService:
    """Service for managing ChromaDB collections and embeddings"""

    def __init__(self, collection_name: str = "web-scraping"):
        self.collection_name = collection_name
        try:
            # Get or create collection
            self.collection = client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
        except Exception as e:
            print(f"Error initializing ChromaDB: {e}")
            self.collection = None

    def store_content(self, url: str, content: str, metadata: Optional[dict] = None):
        """
        Store scraped content in ChromaDB

        Args:
            url: The URL that was scraped
            content: The text content extracted from the page
            metadata: Optional metadata (e.g., domain, scrape_date)
        """
        if not self.collection:
            raise Exception("ChromaDB collection not initialized")

        # Create a unique ID based on URL hash
        import hashlib
        doc_id = hashlib.md5(url.encode()).hexdigest()

        # Add to collection
        self.collection.add(
            ids=[doc_id],
            documents=[content],
            metadatas=[{
                "url": url,
                "content_length": len(content),
                **(metadata or {})
            }]
        )

        return {"status": "success", "id": doc_id, "url": url}



    """
    Search for similar content in ChromaDB

            Args:
                query: Search query
                n_results: Number of results to return

            Returns:
                List of matching documents with metadata
    """
    def search_content(self, query: str, n_results: int = 5) -> List[dict]:

        if not self.collection:
            raise Exception("ChromaDB collection not initialized")

        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )

        return results



    """Get collection statistics"""
    def get_stats(self) -> dict:

        if not self.collection:
            return {"error": "ChromaDB not initialized"}

        count = self.collection.count()
        return {
            "collection_name": self.collection_name,
            "document_count": count,
            "status": "healthy" if count >= 0 else "error"
        }

    def delete_collection(self):
        """Delete the collection (use with caution!)"""
        if self.collection:
            client.delete_collection(name=self.collection_name)
            return {"status": "collection deleted"}
        return {"error": "collection not found"}


# Singleton instance for use across the application
chroma_service = ChromaDBService()

