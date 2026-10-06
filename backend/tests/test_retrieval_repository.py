import pytest
from uuid import uuid4

from sqlalchemy import delete

from app.db.session import AsyncSessionLocal
from app.models.chunk import Chunk
from app.models.document import Document
from app.models.embedding import Embedding
from app.retrieval.repository import RetrievalRepository


@pytest.mark.anyio
async def test_similarity_search_ranks_results():

    document_id = uuid4()

    document = Document(
        id=document_id,
        filename="architecture.md",
        source="retrieval-ranking-test",
        content="Enterprise architecture information.",
    )

    async with AsyncSessionLocal() as session:

        # 1. Save document
        session.add(document)
        await session.flush()

        # 2. Create chunks
        chunk_a = Chunk(
            id=uuid4(),
            document_id=document_id,
            chunk_index=0,
            chunk_text="Exact match chunk.",
        )

        chunk_b = Chunk(
            id=uuid4(),
            document_id=document_id,
            chunk_index=1,
            chunk_text="Very similar chunk.",
        )

        chunk_c = Chunk(
            id=uuid4(),
            document_id=document_id,
            chunk_index=2,
            chunk_text="Different chunk.",
        )

        session.add_all([chunk_a, chunk_b, chunk_c])
        await session.flush()

        # 3. Create deterministic test vectors
        query_embedding = [1.0, 0.0, 0.0] + [0.0] * 381

        embedding_a = [1.0, 0.0, 0.0] + [0.0] * 381

        embedding_b = [0.9, 0.435889894, 0.0] + [0.0] * 381

        embedding_c = [0.0, 1.0, 0.0] + [0.0] * 381

        # 4. Save embeddings
        session.add_all(
            [
                Embedding(
                    id=uuid4(),
                    chunk_id=chunk_a.id,
                    model="all-MiniLM-L6-v2",
                    embedding=embedding_a,
                ),
                Embedding(
                    id=uuid4(),
                    chunk_id=chunk_b.id,
                    model="all-MiniLM-L6-v2",
                    embedding=embedding_b,
                ),
                Embedding(
                    id=uuid4(),
                    chunk_id=chunk_c.id,
                    model="all-MiniLM-L6-v2",
                    embedding=embedding_c,
                ),
            ]
        )

        await session.commit()

        # 5. Execute similarity search
        repository = RetrievalRepository(session)

        results = await repository.similarity_search(
            query_embedding=query_embedding,
            top_k=10,
        )

        # 6. Find only the results belonging to this test document
        test_results = [
            result
            for result in results
            if result["document_id"] == document_id
        ]

        # 7. Validate our three test results
        assert len(test_results) == 3

        # 8. Validate ranking order
        assert test_results[0]["chunk_text"] == "Exact match chunk."
        assert test_results[1]["chunk_text"] == "Very similar chunk."
        assert test_results[2]["chunk_text"] == "Different chunk."

        # 9. Validate similarity scores
        assert test_results[0]["similarity"] > test_results[1]["similarity"]
        assert test_results[1]["similarity"] > test_results[2]["similarity"]

        # 10. Clean up test data
        await session.execute(
            delete(Embedding).where(
                Embedding.chunk_id.in_(
                    [chunk_a.id, chunk_b.id, chunk_c.id]
                )
            )
        )

        await session.execute(
            delete(Chunk).where(
                Chunk.document_id == document_id
            )
        )

        await session.execute(
            delete(Document).where(
                Document.id == document_id
            )
        )

        await session.commit()
