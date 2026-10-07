from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.ingestion import ingest_pdf

router = APIRouter()


@router.get("/health", tags=["system"])
async def api_health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "docmind-ai",
        "version": "v1",
    }


@router.get("/status", tags=["system"])
async def status() -> dict[str, str]:
    return {"status": "ready"}


@router.post("/documents/ingest", tags=["documents"])
async def ingest_document(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=415,
            detail="Only PDF documents are supported.",
        )

    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded PDF is empty.",
        )

    try:
        result = ingest_pdf(
            filename=file.filename or "document.pdf",
            file_bytes=file_bytes,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=422,
            detail=f"Unable to process PDF: {exc}",
        ) from exc

    return result
