import re

from app.schemas.documents import DocumentChunk, DocumentPage


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def chunk_pages(
    pages: list[DocumentPage],
    chunk_size: int = 1200,
    chunk_overlap: int = 200,
) -> list[DocumentChunk]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be >= 0 and < chunk_size")

    chunks: list[DocumentChunk] = []
    chunk_index = 0

    for page in pages:
        text = normalize_text(page.text)

        if not text:
            continue

        start = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))
            content = text[start:end].strip()

            if content:
                chunks.append(
                    DocumentChunk(
                        chunk_index=chunk_index,
                        content=content,
                        page_number=page.page_number,
                        source=f"page:{page.page_number}",
                    )
                )
                chunk_index += 1

            if end >= len(text):
                break

            start = end - chunk_overlap

    return chunks
