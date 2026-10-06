from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chunk import Chunk
from app.models.embedding import Embedding


class RetrievalRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def similarity_search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        document_id: UUID | None = None,
    ) -> list[dict]:

        distance = Embedding.embedding.cosine_distance(
            query_embedding
        )

        stmt = (
            select(
                Chunk.id,
                Chunk.document_id,
                Chunk.chunk_index,
                Chunk.chunk_text,
                Embedding.model,
                distance.label("distance"),
            )
            .join(
                Embedding,
                Embedding.chunk_id == Chunk.id,
            )
            .order_by(distance)
            .limit(top_k)
        )

        if document_id is not None:
            stmt = stmt.where(Chunk.document_id == document_id)

        result = await self.session.execute(stmt)

        rows = result.all()

        return [
            {
                "chunk_id": row.id,
                "document_id": row.document_id,
                "chunk_index": row.chunk_index,
                "chunk_text": row.chunk_text,
                "model": row.model,
                "distance": float(row.distance),
                "similarity": 1.0 - float(row.distance),
            }
            for row in rows
        ]
