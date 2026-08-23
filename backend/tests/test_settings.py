from app.core.settings import settings


def test_rag_settings():
    assert settings.rag_chunk_size == 1000
    assert settings.rag_chunk_overlap == 200
