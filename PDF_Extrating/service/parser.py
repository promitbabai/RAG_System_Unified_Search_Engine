from pathlib import Path
from docling.document_converter import DocumentConverter

import os

os.environ["HF_HOME"] = r"D:\Workspace\RAG_Integration\SamplePDF\hf_cache"
os.environ["TRANSFORMERS_CACHE"] = r"D:\Workspace\RAG_Integration\SamplePDF\hf_cache"

converter = DocumentConverter()

result = converter.convert("D:/Workspace/RAG_Integration/SamplePDF/Sample.pdf")

markdown = result.document.export_to_markdown()

Path("output").mkdir(exist_ok=True)

with open("output/document.md", "w", encoding="utf-8") as f:
    f.write(markdown)