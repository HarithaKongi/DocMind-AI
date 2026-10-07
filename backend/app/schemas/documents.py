from pydantic import BaseModel, Field


class DocumentPage(BaseModel):
    page_number: int = Field(ge=1)
    text: str


class DocumentChunk(BaseModel):
    chunk_index: int = Field(ge=0)
    content: str
    page_number: int = Field(ge=1)
    source: str


class IngestionResult(BaseModel):
    filename: str
    page_count: int = Field(ge=0)
    character_count: int = Field(ge=0)
    chunk_count: int = Field(ge=0)
    pages: list[DocumentPage]
    chunks: list[DocumentChunk]
