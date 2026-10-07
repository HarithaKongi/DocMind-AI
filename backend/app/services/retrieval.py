from app.repositories.supabase_vector_store import SupabaseVectorStore
from app.schemas.retrieval import RetrievalRequest, RetrievalResponse
from app.services.embeddings import embedding_provider


async def retrieve(
    access_token: str,
    request: RetrievalRequest,
) -> RetrievalResponse:
    query_embedding = (await embedding_provider.embed([request.query]))[0]

    vector_store = SupabaseVectorStore(access_token)

    results = await vector_store.similarity_search(
        query_embedding=query_embedding,
        top_k=request.top_k,
        document_ids=request.document_ids or None,
    )

    return RetrievalResponse(
        query=request.query,
        results=results,
    )
