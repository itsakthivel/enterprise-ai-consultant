from uuid import uuid4

import pytest
from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.models.chunk import Chunk
from app.models.document import Document
from app.models.embedding import Embedding
from app.rag.embedder import Embedder


@pytest.mark.anyio
async def test_store_and_read_embedding():
    document_id = uuid4()
    chunk_id = uuid4()

    document = Document(
        id=document_id,
        filename="embedding-test.md",
        source="test",
        content="The application uses FastAPI.",
    )

    chunk = Chunk(
        id=chunk_id,
        document_id=document_id,
        chunk_index=0,
        chunk_text="The application uses FastAPI.",
    )

    embedder = Embedder()

    vector = embedder.embed_text(
        chunk.chunk_text
    )

    embedding = Embedding(
        chunk_id=chunk_id,
        model="all-MiniLM-L6-v2",
        embedding=vector,
    )

    async with AsyncSessionLocal() as session:
        # 1. Save document first
        session.add(document)
        await session.flush()

        # 2. Save chunk second
        session.add(chunk)
        await session.flush()

        # 3. Save embedding third
        session.add(embedding)
        await session.commit()

        # 4. Read embedding back
        result = await session.execute(
            select(Embedding).where(
                Embedding.chunk_id == chunk_id
            )
        )

        saved_embedding = result.scalar_one()

        assert saved_embedding.chunk_id == chunk_id
        assert saved_embedding.model == "all-MiniLM-L6-v2"
        assert len(saved_embedding.embedding) == 384
