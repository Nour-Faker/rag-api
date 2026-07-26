# RAG PDF Q&A API

Upload PDFs and ask questions. Answers are grounded in your documents.

## Stack
- FastAPI
- ChromaDB (cosine similarity)
- Nomic embeddings via Ollama
- Cross-encoder reranking
- Docker

## Run
docker compose up --build

## Endpoints
POST /api/v1/upload — upload PDF
POST /api/v1/ask   — ask question
GET  /health       — health check