from abc import ABC, abstractmethod

from app.schemas.retrieval import RetrievedChunk


class VectorStore(ABC):
    """Database-agnostic contract for vector storage and similarity search."""

    @abstractmethod
    async def add_chunks(
        self,
        document_id: str,
        chunks: list[dict],
        embeddings: list[list[float]],
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def similarity_search(
        self,
        query_embedding: list[float],
        top_k: int,
        document_ids: list[str] | None = None,
    ) -> list[RetrievedChunk]:
        raise NotImplementedError
