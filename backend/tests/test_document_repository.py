from uuid import uuid4

import pytest
from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.models.document import Document


@pytest.mark.anyio
async def test_create_and_read_document():
    document_id = uuid4()

    document = Document(
        id=document_id,
        filename="test.md",
        source="test",
        content="This is a test document.",
    )

    async with AsyncSessionLocal() as session:
        session.add(document)
        await session.commit()

        result = await session.execute(
            select(Document).where(
                Document.id == document_id
            )
        )

        saved_document = result.scalar_one()

        assert saved_document.id == document_id
        assert saved_document.filename == "test.md"
        assert saved_document.content == "This is a test document."
