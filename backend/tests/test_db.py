import pytest
from sqlalchemy import text

from app.db.session import AsyncSessionLocal


@pytest.mark.anyio
async def test_database_connection():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            text("SELECT 1")
        )

        assert result.scalar() == 1
