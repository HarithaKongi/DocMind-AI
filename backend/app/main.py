from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Backend API for DocMind AI, a citation-grounded RAG knowledge assistant.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["system"])
async def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.app_env,
    }


@app.get(settings.api_v1_prefix + "/health", tags=["system"])
async def api_health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": "v1",
    }
