import re
from uuid import uuid4

from app.core.settings import settings
from app.rag.schemas import Chunk, Document


def _split_into_sentences(text: str) -> list[str]:
    """Split text into sentences."""
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def _split_long_text(text: str, max_size: int) -> list[str]:
    """
    Split oversized text using word boundaries.

    A word is split by character only when the word itself
    is longer than max_size.
    """
    words = text.split()
    parts = []
    current_words = []
    current_length = 0

    for word in words:
        separator_length = 1 if current_words else 0
        candidate_length = (
            current_length
            + separator_length
            + len(word)
        )

        if candidate_length <= max_size:
            current_words.append(word)
            current_length = candidate_length
            continue

        if current_words:
            parts.append(" ".join(current_words))

        if len(word) > max_size:
            for start in range(0, len(word), max_size):
                parts.append(word[start:start + max_size])

            current_words = []
            current_length = 0
        else:
            current_words = [word]
            current_length = len(word)

    if current_words:
        parts.append(" ".join(current_words))

    return parts


def _prepare_units(text: str, max_size: int) -> list[str]:
    """
    Create semantic units using:

    paragraph → sentence → word
    """
    paragraphs = re.split(r"\n\s*\n", text.strip())

    units = []

    for paragraph in paragraphs:
        paragraph = paragraph.strip()

        if not paragraph:
            continue

        if len(paragraph) <= max_size:
            units.append(paragraph)
            continue

        sentences = _split_into_sentences(paragraph)

        for sentence in sentences:
            if len(sentence) <= max_size:
                units.append(sentence)
            else:
                units.extend(
                    _split_long_text(sentence, max_size)
                )

    return units


def _calculate_length(units: list[str]) -> int:
    """Calculate text length including paragraph separators."""
    if not units:
        return 0

    return sum(len(unit) for unit in units) + (
        2 * (len(units) - 1)
    )


def _build_overlap(
    units: list[str],
    overlap: int,
) -> list[str]:
    """
    Build overlap using complete semantic units.

    We never slice an individual unit to achieve overlap.
    """
    if overlap <= 0:
        return []

    selected = []
    length = 0

    for unit in reversed(units):
        additional_length = len(unit)

        if selected:
            additional_length += 2

        if length + additional_length > overlap:
            break

        selected.insert(0, unit)
        length += additional_length

    return selected


def chunk_document(
    document: Document,
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:

    max_size = (
        chunk_size
        if chunk_size is not None
        else settings.rag_chunk_size
    )

    chunk_overlap = (
        overlap
        if overlap is not None
        else settings.rag_chunk_overlap
    )

    if max_size <= 0:
        raise ValueError(
            "chunk_size must be greater than zero"
        )

    if chunk_overlap < 0:
        raise ValueError(
            "overlap cannot be negative"
        )

    if chunk_overlap >= max_size:
        raise ValueError(
            "overlap must be smaller than chunk_size"
        )

    units = _prepare_units(
        document.content,
        max_size,
    )

    chunks = []
    current_units = []

    for unit in units:

        candidate_units = current_units + [unit]

        if (
            _calculate_length(candidate_units)
            <= max_size
        ):
            current_units.append(unit)
            continue

        # Save current chunk.
        if current_units:
            chunks.append(
                Chunk(
                    id=str(uuid4()),
                    document_id=document.id,
                    chunk_index=len(chunks),
                    chunk_text="\n\n".join(
                        current_units
                    ),
                )
            )

        # Build semantic overlap.
        overlap_units = _build_overlap(
            current_units,
            chunk_overlap,
        )

        current_units = overlap_units + [unit]

    # Final chunk.
    if current_units:
        chunks.append(
            Chunk(
                id=str(uuid4()),
                document_id=document.id,
                chunk_index=len(chunks),
                chunk_text="\n\n".join(
                    current_units
                ),
            )
        )

    return chunks
