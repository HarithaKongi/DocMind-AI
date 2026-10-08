from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.api.dependencies import get_current_user
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.retrieval import RetrievalRequest, RetrievalResponse
from app.services.generation import chat
from app.services.indexing import index_pdf
from app.services.retrieval import retrieve

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
async def ingest_document(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
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
        return await index_pdf(
            access_token=current_user["access_token"],
            user_id=current_user["id"],
            filename=file.filename or "document.pdf",
            file_bytes=file_bytes,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=422,
            detail=f"Unable to index PDF: {exc}",
        ) from exc


@router.post(
    "/retrieval/search",
    response_model=RetrievalResponse,
    tags=["retrieval"],
)
async def semantic_search(
    request: RetrievalRequest,
    current_user: dict = Depends(get_current_user),
):
    try:
        return await retrieve(
            access_token=current_user["access_token"],
            request=request,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=422,
            detail=f"Unable to perform semantic search: {exc}",
        ) from exc


@router.post(
    "/chat",
    response_model=ChatResponse,
    tags=["chat"],
)
async def document_chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
):
    try:
        return await chat(
            access_token=current_user["access_token"],
            request=request,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=422,
            detail=f"Unable to generate grounded answer: {exc}",
        ) from exc
