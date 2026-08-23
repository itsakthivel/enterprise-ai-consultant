from app.rag.schemas import Document
from app.rag.text_chunker import chunk_document


def test_chunk_document():
    document = Document(
        id="doc-1",
        filename="test.md",
        source="test",
        content=(
            "The platform uses FastAPI and PostgreSQL.\n\n"
            "The application is deployed using Docker and Kubernetes.\n\n"
            "Secrets should never be stored in source code."
        ),
    )

    chunks = chunk_document(document)

    assert len(chunks) > 0

    for chunk in chunks:
        assert chunk.document_id == "doc-1"
        assert chunk.chunk_text.strip()


def test_chunker_does_not_split_words():
    document = Document(
        id="doc-2",
        filename="test.md",
        source="test",
        content=(
            "The application is deployed using Docker and Kubernetes. "
            "The deployment process requires configuration management."
        ),
    )

    chunks = chunk_document(
        document,
        chunk_size=50,
        overlap=10,
    )

    for chunk in chunks:
        assert not chunk.chunk_text.endswith("de")
        assert not chunk.chunk_text.startswith("ployed")


def test_chunk_document_preserves_document_id():
    document = Document(
        id="document-123",
        filename="architecture.md",
        source="test",
        content="FastAPI is used for building REST APIs.",
    )

    chunks = chunk_document(document)

    for chunk in chunks:
        assert chunk.document_id == "document-123"


def test_chunker_respects_word_boundaries():
    document = Document(
        id="doc-3",
        filename="test.md",
        source="test",
        content=(
            "The application is deployed using Docker and Kubernetes. "
            "The deployment process requires configuration management."
        ),
    )

    chunks = chunk_document(
        document,
        chunk_size=50,
        overlap=10,
    )

    for chunk in chunks:
        assert not chunk.chunk_text.endswith("de")
        assert not chunk.chunk_text.startswith("ployed")
