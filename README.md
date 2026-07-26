# 🔍 RAG PDF Q&A API

> Upload any PDF and ask questions about it. Answers are grounded in your document with source citations.

## ✨ Features

- **PDF Ingestion** — upload any PDF, automatically chunked and indexed
- **Semantic Search** — cosine similarity search with ChromaDB
- **Cross-encoder Reranking** — reranks retrieved chunks for better relevance
- **Source Citations** — every answer includes the exact chunks it came from
- **Local & Private** — runs entirely on your machine via Ollama, no data sent externally
- **Dockerized** — one command to run

## 🏗️ Architecture
PDF Upload → Text Extraction → Recursive Chunking → Nomic Embeddings
↓
User Question → Embed Query → ChromaDB Search → Cross-encoder Rerank → LLM → Answer + Sources
## 🛠️ Stack

| Layer | Technology |
|---|---|
| API | FastAPI |
| Vector DB | ChromaDB (cosine similarity) |
| Embeddings | nomic-embed-text via Ollama |
| Reranking | cross-encoder/ms-marco-MiniLM-L-6-v2 |
| LLM | tinyllama via Ollama |
| Deployment | Docker + docker-compose |

## 🚀 Quick Start

### Prerequisites
- Docker + Docker Compose
- [Ollama](https://ollama.ai) running locally with these models:
```bash
ollama pull nomic-embed-text
ollama pull tinyllama
```

### Run
```bash
git clone https://github.com/Nour-Faker/rag-api
cd rag-api
docker compose up --build
```

API available at `http://localhost:8000`
Swagger UI at `http://localhost:8000/docs`

## 📡 API Endpoints

### Upload a PDF
```bash
curl -X POST http://localhost:8000/api/v1/upload \
  -F "file=@your_document.pdf"
```

Response:
```json
{
  "doc_id": "uuid-here",
  "chunks_stored": 87,
  "filename": "your_document.pdf",
  "message": "Successfully processed your_document.pdf"
}
```

### Ask a Question
```bash
curl -X POST http://localhost:8000/api/v1/ask \
  -H "Content-Type: application/json" \
  -d '{"doc_id": "uuid-here", "question": "What is the main topic?"}'
```

Response:
```json
{
  "answer": "According to chunk 3, the document discusses...",
  "sources": [
    {
      "text": "relevant chunk text...",
      "chunk_index": 3,
      "similarity": 0.847,
      "rerank_score": 8.42,
      "source": "your_document.pdf"
    }
  ],
  "doc_id": "uuid-here"
}
```

## 📁 Project Structure
rag-api/
├── app/
│ ├── routers/
│ │ ├── upload.py # PDF ingestion endpoint
│ │ └── ask.py # Q&A endpoint with reranking
│ ├── services/
│ │ ├── chunker.py # recursive text splitting
│ │ ├── embedder.py # nomic embeddings via Ollama
│ │ ├── retriever.py # ChromaDB vector search
│ │ ├── reranker.py # cross-encoder reranking
│ │ └── pdf.py # PDF text extraction
│ ├── main.py
│ └── models.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt

