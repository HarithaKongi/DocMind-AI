from app.repositories.supabase_vector_store import SupabaseVectorStore
from app.schemas.retrieval import RetrievalRequest, RetrievalResponse


async def retrieve(request: RetrievalRequest) -> RetrievalResponse:
    raise RuntimeError(
        "Embedding generation is not configured yet. "
        "The vector store is ready for the embedding provider."
    )
