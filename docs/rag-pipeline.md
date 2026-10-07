# RAG Pipeline

## Ingestion

PDF -> text extraction -> page-aware chunking -> embeddings -> pgvector

Each chunk will retain enough metadata to map an answer back to its source document and page.

## Retrieval

Question -> query embedding -> vector similarity search -> top-K candidates -> optional reranking.

## Generation

The selected passages and user question are assembled into a constrained prompt. The LLM generates an answer using the retrieved evidence.

## Citations

Every returned citation should identify the source document and page, with an excerpt where appropriate.

## Future Engineering Work

- Hybrid lexical + vector retrieval
- Reranking
- Context filtering
- Prompt-injection defenses
- Caching
- Retrieval evaluation
- Answer faithfulness evaluation
