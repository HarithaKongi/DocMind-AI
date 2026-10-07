from abc import ABC, abstractmethod

import httpx

from app.core.config import settings


class EmbeddingProvider(ABC):
    """Provider-agnostic interface for generating embedding vectors."""

    @property
    @abstractmethod
    def dimensions(self) -> int:
        raise NotImplementedError

    @abstractmethod
    async def embed(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError


class HostedEmbeddingProvider(EmbeddingProvider):
    def __init__(
        self,
        api_key: str,
        api_url: str,
        model: str,
        dimensions: int,
    ) -> None:
        self.api_key = api_key
        self.api_url = api_url
        self.model = model
        self._dimensions = dimensions

    @property
    def dimensions(self) -> int:
        return self._dimensions

    async def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        if not self.api_key:
            raise RuntimeError(
                "EMBEDDING_API_KEY is not configured."
            )

        payload = {
            "model": self.model,
            "input": texts,
        }

        response = await _post_embeddings(
            self.api_url,
            self.api_key,
            payload,
        )

        data = response.get("data", [])

        if len(data) != len(texts):
            raise RuntimeError(
                "Embedding provider returned an unexpected number of vectors."
            )

        vectors = [item["embedding"] for item in data]

        if any(len(vector) != self.dimensions for vector in vectors):
            raise RuntimeError(
                f"Expected {self.dimensions}-dimensional embeddings."
            )

        return vectors


async def _post_embeddings(
    api_url: str,
    api_key: str,
    payload: dict,
) -> dict:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            api_url,
            json=payload,
            headers=headers,
        )

    if response.is_error:
        detail = response.text[:500]
        raise RuntimeError(
            f"Embedding provider request failed ({response.status_code}): {detail}"
        )

    return response.json()


embedding_provider = HostedEmbeddingProvider(
    api_key=settings.embedding_api_key,
    api_url=settings.embedding_api_url,
    model=settings.embedding_model,
    dimensions=settings.embedding_dimensions,
)
