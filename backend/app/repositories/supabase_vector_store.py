from app.core.supabase import supabase_rest
from app.repositories.vector_store import VectorStore
from app.schemas.retrieval import RetrievedChunk


class SupabaseVectorStore(VectorStore):
    def __init__(self, access_token: str) -> None:
        self.access_token = access_token

    async def add_chunks(self, document_id: str, chunks: list[dict], embeddings: list[list[float]]) -> None:
        if len(chunks) != len(embeddings):
            raise ValueError("chunks and embeddings must have the same length")
        rows = [
            {"document_id": document_id, "chunk_index": chunk["chunk_index"],
             "content": chunk["content"], "page_number": chunk["page_number"],
             "embedding": embedding, "metadata": chunk.get("metadata", {})}
            for chunk, embedding in zip(chunks, embeddings)
        ]
        await supabase_rest("POST", "/rest/v1/document_chunks", self.access_token, json=rows)

    async def similarity_search(self, query_embedding: list[float], top_k: int,
                                document_ids: list[str] | None = None) -> list[RetrievedChunk]:
        response = await supabase_rest(
            "POST", "/rest/v1/rpc/match_document_chunks", self.access_token,
            json={"query_embedding": query_embedding, "match_threshold": 0.70,
                  "match_count": top_k, "filter_document_ids": document_ids or None},
        )
        return [
            RetrievedChunk(chunk_id=str(row["chunk_id"]), document_id=str(row["document_id"]),
                           content=row["content"], page_number=row["page_number"],
                           similarity=row["similarity"])
            for row in (response.json() or [])
        ]
