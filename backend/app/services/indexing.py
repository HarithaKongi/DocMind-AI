from app.repositories.documents import SupabaseDocumentRepository
from app.repositories.supabase_vector_store import SupabaseVectorStore
from app.services.embeddings import embedding_provider
from app.services.ingestion import ingest_pdf


async def index_pdf(
    access_token: str,
    user_id: str,
    filename: str,
    file_bytes: bytes,
) -> dict:
    document_repository = SupabaseDocumentRepository(access_token)
    vector_store = SupabaseVectorStore(access_token)

    result = ingest_pdf(
        filename=filename,
        file_bytes=file_bytes,
    )

    document_id = await document_repository.create(
        user_id=user_id,
        filename=filename,
        file_size=len(file_bytes),
        page_count=result.page_count,
    )

    try:
        texts = [chunk.content for chunk in result.chunks]

        if not texts:
            raise ValueError("No extractable text was found in the PDF.")

        embeddings = await embedding_provider.embed(texts)

        chunks = [
            {
                "chunk_index": chunk.chunk_index,
                "content": chunk.content,
                "page_number": chunk.page_number,
                "metadata": {"source": chunk.source},
            }
            for chunk in result.chunks
        ]

        await vector_store.add_chunks(
            document_id=document_id,
            chunks=chunks,
            embeddings=embeddings,
        )

        await document_repository.update_status(
            document_id=document_id,
            status="ready",
        )

        return {
            "document_id": document_id,
            "filename": filename,
            "page_count": result.page_count,
            "chunk_count": result.chunk_count,
            "status": "ready",
        }

    except Exception as exc:
        await document_repository.update_status(
            document_id=document_id,
            status="failed",
            error_message=str(exc)[:1000],
        )
        raise
