from uuid import uuid4

import pytest
from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.models.chunk import Chunk
from app.models.document import Document


@pytest.mark.anyio
async def test_create_document_with_chunks():
    document_id = uuid4()

    document = Document(
        id=document_id,
        filename="architecture.md",
        source="test",
        content="Test architecture document.",
    )

    chunk_1 = Chunk(
        document_id=document_id,
        chunk_index=0,
        chunk_text="The platform uses FastAPI.",
    )

    chunk_2 = Chunk(
        document_id=document_id,
        chunk_index=1,
        chunk_text="The platform uses PostgreSQL.",
    )

    async with AsyncSessionLocal() as session:
        session.add(document)
        session.add_all([chunk_1, chunk_2])

        await session.commit()

        result = await session.execute(
            select(Chunk)
            .where(Chunk.document_id == document_id)
            .order_by(Chunk.chunk_index)
        )

        chunks = result.scalars().all()

        assert len(chunks) == 2
        assert chunks[0].chunk_index == 0
        assert chunks[1].chunk_index == 1
        assert chunks[0].chunk_text == "The platform uses FastAPI."
        assert chunks[1].chunk_text == "The platform uses PostgreSQL."
