from datetime import datetime, UTC
from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4

from app.models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.chunk import Chunk

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    source: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    chunks: Mapped[list["Chunk"]] = relationship(
        "Chunk",
        back_populates="document",
        cascade="all, delete-orphan",
    )
