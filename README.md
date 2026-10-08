# DocMind AI

> Production-style RAG knowledge assistant for asking questions over documents with citation-grounded answers.

DocMind AI lets users upload documents, ask questions in natural language, and receive answers grounded in retrieved passages with page-level citations.

## Planned Stack

- **Frontend:** Next.js + TypeScript
- **Backend:** Python + FastAPI
- **Database:** PostgreSQL + pgvector
- **Auth & Storage:** Supabase
- **LLM:** Provider-agnostic LLM API
- **Infrastructure:** Docker
- **CI:** GitHub Actions

## Architecture

```
Next.js
   |
   v
FastAPI
   |
   +--> Document ingestion --> Embeddings --> PostgreSQL + pgvector
   |
   +--> Retrieval --> Reranking --> LLM --> Grounded answer + citations
```

## Repository Layout

- `frontend/` — web application
- `backend/` — API and RAG engine
- `evaluation/` — retrieval and answer-quality evaluation
- `docs/` — architecture and engineering documentation
- `infrastructure/` — container and deployment configuration

## Status

🚧 Backend RAG foundation and the first frontend vertical slice are implemented.

### Frontend vertical slice

The `frontend/` application now provides:

- Supabase email/password sign-up and sign-in
- Authenticated dashboard
- PDF-only upload validation
- Automatic Supabase access-token forwarding to the FastAPI ingestion endpoint
- Upload/indexing status feedback

The frontend uses only the public Supabase client key. Never commit `.env` files or secret API keys.

## Author

**Haritha Kongi**

Designed and developed as an AI engineering portfolio project.
