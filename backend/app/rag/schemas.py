from pydantic import BaseModel


class Document(BaseModel):
    id: str
    filename: str
    source: str
    content: str


class Chunk(BaseModel):
    id: str
    document_id: str
    chunk_index: int
    chunk_text: str
