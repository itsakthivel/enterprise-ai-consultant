from app.rag.embedder import Embedder


def test_embed_text():
    embedder = Embedder()

    embedding = embedder.embed_text(
        "The application uses FastAPI."
    )

    assert isinstance(embedding, list)
    assert len(embedding) == 384


def test_embed_texts():
    embedder = Embedder()

    texts = [
        "The application uses FastAPI.",
        "PostgreSQL stores enterprise data.",
        "Docker is used for deployment.",
    ]

    embeddings = embedder.embed_texts(texts)

    assert len(embeddings) == 3

    for embedding in embeddings:
        assert isinstance(embedding, list)
        assert len(embedding) == 384


def test_similarity():
    embedder = Embedder()

    similar_text_a = "The application uses FastAPI."
    similar_text_b = "FastAPI is used by the application."
    unrelated_text = "The weather is sunny today."

    embedding_a = embedder.embed_text(similar_text_a)
    embedding_b = embedder.embed_text(similar_text_b)
    embedding_c = embedder.embed_text(unrelated_text)

    similar_score = embedder.similarity(
        embedding_a,
        embedding_b,
    )

    unrelated_score = embedder.similarity(
        embedding_a,
        embedding_c,
    )

    assert similar_score > unrelated_score
