from app.rag.document_loader import load_document
from app.rag.embedder import Embedder
from app.rag.text_chunker import chunk_document


def test_document_to_embeddings():
    document = load_document(
        "sample_docs/architecture.md"
    )

    chunks = chunk_document(document)

    embedder = Embedder()

    texts = [
        chunk.chunk_text
        for chunk in chunks
    ]

    embeddings = embedder.embed_texts(texts)

    assert len(embeddings) == len(chunks)

    for chunk, embedding in zip(chunks, embeddings):
        assert chunk.chunk_text
        assert len(embedding) == 384
