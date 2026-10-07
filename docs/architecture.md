# DocMind AI Architecture

## System Overview

DocMind AI is a retrieval-augmented generation (RAG) application.

### Request flow

1. The user uploads a document through the Next.js frontend.
2. FastAPI validates and processes the document.
3. Text is extracted with page metadata preserved.
4. Text is split into retrieval-friendly chunks.
5. Chunks are embedded and stored in PostgreSQL with pgvector.
6. A user question is embedded and matched against stored chunks.
7. Relevant chunks are optionally reranked.
8. The selected context is sent to the LLM.
9. The API returns a grounded answer and source citations.

## Architectural Boundaries

- **Frontend:** presentation, authentication state, document/chat UX.
- **Backend:** API orchestration, validation, business logic and RAG pipeline.
- **Database:** users' document metadata, chunks, embeddings and conversations.
- **Storage:** original uploaded documents.
- **Evaluation:** reproducible tests for retrieval and generation quality.

## Design Principles

- Keep frontend and RAG logic separated.
- Preserve document/page metadata throughout ingestion.
- Never expose provider API keys to the browser.
- Scope user data by authenticated user identity.
- Make retrieval and generation independently testable.
- Design for provider replacement where practical.
