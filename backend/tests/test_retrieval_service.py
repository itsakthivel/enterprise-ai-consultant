from uuid import uuid4

import pytest

from app.db.session import AsyncSessionLocal
from app.models.chunk import Chunk
from app.models.document import Document
from app.models.embedding import Embedding
from app.rag.embedder import Embedder
from app.retrieval.service import RetrievalService


class FakeEmbedder:
    def embed_text(self, text: str) -> list[float]:
        return [1.0, 0.0, 0.0] + [0.0] * 381


@pytest.mark.anyio
async def test_retrieval_service_search():

    document_id = uuid4()

    document = Document(
        id=document_id,
        filename="service-test.md",
        source="retrieval-service-test",
        content="Enterprise architecture information.",
    )

    async with AsyncSessionLocal() as session:

        session.add(document)
        await session.flush()

        chunk = Chunk(
            id=uuid4(),
            document_id=document_id,
            chunk_index=0,
            chunk_text="Exact match chunk.",
        )

        session.add(chunk)
        await session.flush()

        embedding = Embedding(
            id=uuid4(),
            chunk_id=chunk.id,
            model="all-MiniLM-L6-v2",
            embedding=[1.0, 0.0, 0.0] + [0.0] * 381,
        )

        session.add(embedding)

        chunk_id = chunk.id
        await session.commit()

        service = RetrievalService(
            session=session,
            embedder=FakeEmbedder(),
        )

        response = await service.search(
            query="How is the application deployed?",
            top_k=1,
            document_id=document_id,
        )

        assert response.query == "How is the application deployed?"
        assert len(response.results) == 1
        assert response.results[0].chunk_id == chunk_id
        assert response.results[0].document_id == document_id
        assert response.results[0].chunk_text == "Exact match chunk."
        assert response.results[0].similarity == pytest.approx(1.0)


@pytest.mark.anyio
async def test_retrieval_service_rejects_empty_query():

    async with AsyncSessionLocal() as session:

        service = RetrievalService(
            session=session,
            embedder=FakeEmbedder(),
        )

        with pytest.raises(
            ValueError,
            match="Query must not be empty",
        ):
            await service.search(
                query="   ",
                top_k=5,
            )


@pytest.mark.anyio
async def test_retrieval_service_rejects_invalid_top_k():

    async with AsyncSessionLocal() as session:

        service = RetrievalService(
            session=session,
            embedder=FakeEmbedder(),
        )

        with pytest.raises(
            ValueError,
            match="top_k must be greater than zero",
        ):
            await service.search(
                query="deployment",
                top_k=0,
            )
