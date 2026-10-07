from app.schemas.documents import IngestionResult
from app.services.chunker import chunk_pages
from app.services.pdf_extractor import extract_pdf_pages


def ingest_pdf(
    filename: str,
    file_bytes: bytes,
    chunk_size: int = 1200,
    chunk_overlap: int = 200,
) -> IngestionResult:
    pages = extract_pdf_pages(file_bytes)
    chunks = chunk_pages(
        pages,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    character_count = sum(len(page.text) for page in pages)

    return IngestionResult(
        filename=filename,
        page_count=len(pages),
        character_count=character_count,
        chunk_count=len(chunks),
        pages=pages,
        chunks=chunks,
    )
