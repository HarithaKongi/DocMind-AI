from pydantic import BaseModel, Field


class Citation(BaseModel):
    document_id: str
    page_number: int = Field(ge=1)
    excerpt: str


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)
    document_ids: list[str] = Field(default_factory=list)
    top_k: int = Field(default=5, ge=1, le=10)


class ChatResponse(BaseModel):
    answer: str
    grounded: bool
    citations: list[Citation]
