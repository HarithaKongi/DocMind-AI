# Vector Search

DocMind AI will use PostgreSQL with pgvector for semantic retrieval.

## Indexing

1. Extract page-aware document chunks.
2. Generate one embedding vector per chunk.
3. Store the chunk, document ID, page number and embedding.
4. Build a vector index for similarity search.

## Querying

1. Generate an embedding for the user's question.
2. Compare the query vector with stored chunk vectors.
3. Return the top-K most similar chunks.
4. Preserve document and page metadata for citations.

## Design Decision

The application uses provider interfaces instead of coupling the RAG pipeline directly to one embedding vendor. This allows the project to switch between hosted embeddings and local models without rewriting retrieval logic.

## Planned database function

The eventual pgvector search function will accept:

- query embedding
- requested top-K
- optional document IDs
- authenticated user scope

It will return similarity scores and citation metadata.
