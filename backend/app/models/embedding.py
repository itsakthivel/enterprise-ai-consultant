from datetime import datetime, UTC
from uuid import UUID, uuid4

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.chunk import Chunk
    
class Embedding(Base):

    __tablename__ = "embeddings"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    chunk_id: Mapped[UUID] = mapped_column(
        ForeignKey("chunks.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    model: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(384),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    chunk: Mapped["Chunk"] = relationship(
        "Chunk",
        back_populates="embedding",
    )
