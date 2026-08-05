
import chromadb
from chromadb import QueryResult

client = chromadb.HttpClient(
    host="chromadb",
    port=8000
)

def query() -> str:
    collection = client.get_or_create_collection("documents")

    collection.add(
        ids=["1"],
        documents=["This is a sample document"]
    )

    results:QueryResult = collection.query(
        query_texts=["sample"],
        n_results=1
    )
    return results.__str__()
