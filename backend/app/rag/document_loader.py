from pathlib import Path
from uuid import uuid4

from app.rag.schemas import Document


def load_document(file_path: str) -> Document:
    path = Path(file_path)

    content = path.read_text(encoding="utf-8")

    return Document(
        id=str(uuid4()),
        filename=path.name,
        source=str(path.parent),
        content=content,
    )
