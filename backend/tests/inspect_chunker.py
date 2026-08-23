from app.rag.document_loader import load_document
from app.rag.text_chunker import chunk_document


document = load_document("sample_docs/architecture.md")

chunks = chunk_document(document)

for chunk in chunks:
    print(f"\n--- Chunk {chunk.chunk_index} ---")
    print(chunk.chunk_text)
