from langchain_text_splitters import RecursiveCharacterTextSplitter


# 1. Initialize the splitter (Do this globally or inside a config/init)
# Adjust chunk_size based on your embedding model (e.g., text-embedding-3-small handles 8k, but 500-1000 is sweet spot for retrieval)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,       # Maximum characters per chunk
    chunk_overlap=200,     # Overlap between consecutive chunks to maintain context
    separators=["\n\n", "\n", " ", ""] # Order of priority for splitting
)


def process_and_chunk_page(textOfHtmlPage: str):

    # 2. Generate the chunks
    chunks = text_splitter.split_text(textOfHtmlPage)

    # 3. Structure them for your Vector DB (Optional but recommended)
    # Usually, you want to store metadata alongside the chunks
    structured_chunks = []
    for i, chunk in enumerate(chunks):
        structured_chunks.append({
            "chunk_id": f"chunk_{i}",
            "text": chunk,
            "metadata": {
                "index": i,
                "length": len(chunk)
                # You can add "url": url, "title": title here later
            }
        })
        print (structured_chunks[i])
        print("\n------------------------------------------------------------------------\n")