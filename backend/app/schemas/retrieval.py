from pydantic import BaseModel, Field


class RetrievedChunk(BaseModel):
    chunk_id: str
    document_id: str
    content: str
    page_number: int = Field(ge=1)
    similarity: float = Field(ge=-1, le=1)


class RetrievalRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2000)
    document_ids: list[str] = Field(default_factory=list)
    top_k: int = Field(default=5, ge=1, le=20)


class RetrievalResponse(BaseModel):
    query: str
    results: list[RetrievedChunk]
