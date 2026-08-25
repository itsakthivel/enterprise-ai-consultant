from app.core.settings import settings


def test_rag_settings():
    assert settings.rag_chunk_size == 1000
    assert settings.rag_chunk_overlap == 200
    assert settings.embedding_model == "all-MiniLM-L6-v2"
