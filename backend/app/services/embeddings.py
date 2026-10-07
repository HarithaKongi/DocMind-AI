from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    """Provider-agnostic interface for generating embedding vectors."""

    @property
    @abstractmethod
    def dimensions(self) -> int:
        raise NotImplementedError

    @abstractmethod
    async def embed(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError


class NotConfiguredEmbeddingProvider(EmbeddingProvider):
    """Placeholder until a real embedding provider is configured."""

    @property
    def dimensions(self) -> int:
        return 0

    async def embed(self, texts: list[str]) -> list[list[float]]:
        raise RuntimeError(
            "No embedding provider is configured. "
            "Configure an embedding provider before indexing documents."
        )


embedding_provider = NotConfiguredEmbeddingProvider()
