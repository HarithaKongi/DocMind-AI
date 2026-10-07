from fastapi import APIRouter

router = APIRouter()


@router.get("/status", tags=["system"])
async def status() -> dict[str, str]:
    return {"status": "ready"}
