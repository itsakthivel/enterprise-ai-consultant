from uuid import UUID

from pydantic import BaseModel, Field


class RetrievalResult(BaseModel):
    chunk_id: UUID
    document_id: UUID
    chunk_index: int
    chunk_text: str
    model: str
    distance: float
    similarity: float


class RetrievalResponse(BaseModel):
    query: str
    results: list[RetrievalResult]
