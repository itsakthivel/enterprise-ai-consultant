from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.rag.embedder import Embedder
from app.retrieval.repository import RetrievalRepository
from app.retrieval.schemas import RetrievalResponse, RetrievalResult


class RetrievalService:
    def __init__(
        self,
        session: AsyncSession,
        embedder: Embedder | None = None,
    ):
        self.repository = RetrievalRepository(session)
        self.embedder = embedder or Embedder()

    async def search(
        self,
        query: str,
        top_k: int = 5,
        document_id: UUID | None = None,
    ) -> RetrievalResponse:

        if not query.strip():
            raise ValueError("Query must not be empty.")

        if top_k < 1:
            raise ValueError("top_k must be greater than zero.")

        query_embedding = self.embedder.embed_text(query)

        results = await self.repository.similarity_search(
            query_embedding=query_embedding,
            top_k=top_k,
            document_id=document_id,
        )

        retrieval_results = [
            RetrievalResult(**result)
            for result in results
        ]

        return RetrievalResponse(
            query=query,
            results=retrieval_results,
        )
