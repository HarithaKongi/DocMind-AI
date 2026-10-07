from io import BytesIO

from pypdf import PdfReader

from app.schemas.documents import DocumentPage


def extract_pdf_pages(file_bytes: bytes) -> list[DocumentPage]:
    reader = PdfReader(BytesIO(file_bytes))

    pages: list[DocumentPage] = []

    for index, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()

        pages.append(
            DocumentPage(
                page_number=index,
                text=text,
            )
        )

    return pages
