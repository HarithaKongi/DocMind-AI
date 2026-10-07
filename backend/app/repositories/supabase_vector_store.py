from supabase import Client

from app.core.supabase import get_user_supabase_client
from app.repositories.vector_store import VectorStore
from app.schemas.retrieval import RetrievedChunk


class SupabaseVectorStore(VectorStore):
    def __init__(self, access_token: str) -> None:
        self.client: Client = get_user_supabase_client(access_token)

    async def add_chunks(
        self,
        document_id: str,
        chunks: list[dict],
        embeddings: list[list[float]],
    ) -> None:
        if len(chunks) != len(embeddings):
            raise ValueError("chunks and embeddings must have the same length")

        rows = [
            {
                "document_id": document_id,
                "chunk_index": chunk["chunk_index"],
                "content": chunk["content"],
                "page_number": chunk["page_number"],
                "embedding": embedding,
                "metadata": chunk.get("metadata", {}),
            }
            for chunk, embedding in zip(chunks, embeddings)
        ]

        self.client.table("document_chunks").insert(rows).execute()

    async def similarity_search(
        self,
        query_embedding: list[float],
        top_k: int,
        document_ids: list[str] | None = None,
    ) -> list[RetrievedChunk]:
        response = self.client.rpc(
            "match_document_chunks",
            {
                "query_embedding": query_embedding,
                "match_threshold": 0.70,
                "match_count": top_k,
                "filter_document_ids": document_ids or None,
            },
        ).execute()

        return [
            RetrievedChunk(
                chunk_id=str(row["chunk_id"]),
                document_id=str(row["document_id"]),
                content=row["content"],
                page_number=row["page_number"],
                similarity=row["similarity"],
            )
            for row in (response.data or [])
        ]
