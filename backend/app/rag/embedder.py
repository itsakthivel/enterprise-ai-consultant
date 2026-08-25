import numpy as np
from sentence_transformers import SentenceTransformer

from app.core.settings import settings


class Embedder:
    def __init__(self):
        self.model = SentenceTransformer(
            settings.embedding_model
        )

    def embed_text(self, text: str) -> list[float]:
        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed_texts(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
        )

        return embeddings.tolist()

    def similarity(
        self,
        embedding_a: list[float],
        embedding_b: list[float],
    ) -> float:
        vector_a = np.array(embedding_a)
        vector_b = np.array(embedding_b)

        return float(np.dot(vector_a, vector_b))
