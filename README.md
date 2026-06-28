# 🧠 RAG PDF Q&A API

> Upload any PDF. Ask questions in natural language. Get answers grounded in your document — 100% local, zero cost.

![Python](https://img.shields.io/badge/Python-3.14-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-teal)
![ChromaDB](https://img.shields.io/badge/ChromaDB-purple)
![Ollama](https://img.shields.io/badge/Ollama-orange)
![License](https://img.shields.io/badge/License-MIT-gray)

---

## What is RAG?

RAG (Retrieval-Augmented Generation) solves a core LLM limitation — models can't read your documents. Instead of fine-tuning, RAG finds the relevant paragraphs first, then hands them to the LLM as context. The result: factual, grounded answers with source attribution.

---

## Upload flow

```
PDF upload  →  Text chunker     →  Embedder           →  ChromaDB
POST /upload   500-word overlap    nomic-embed-text      vector store
```

## Query flow

```
Question   →  Embed query      →  Top-3 chunks      →  LLM answer
POST /ask     same model          cosine similarity     qwen2.5 local
```

---

## Tech stack

| Tool | Role |
|------|------|
| FastAPI | REST API framework |
| ChromaDB | Vector database |
| Ollama | Local LLM inference |
| nomic-embed-text | Embedding model |
| qwen2.5-coder | Language model |
| pypdf | PDF text extraction |
| Pydantic | Data validation |
| Python 3.14 | Runtime |

---

## Quick start

```bash
# 1. Clone and setup
git clone https://github.com/Nour-Faker/rag-api
cd rag-api
python -m venv venv && source venv/Scripts/activate
python -m pip install -r requirements.txt

# 2. Pull Ollama models
ollama pull nomic-embed-text
ollama pull tinyllama

# 3. Run
python -m uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs` for the interactive Swagger UI.

---

## Endpoints

### `POST /api/v1/upload`
Upload and index a PDF.

**Response:**
```json
{
  "doc_id": "76c0d933-243a-...",
  "chunks_stored": 33,
  "message": "Successfully processed"
}
```

---

### `POST /api/v1/ask`
Ask a question about a document.

**Request:**
```json
{
  "doc_id": "76c0d933-...",
  "question": "What is artificial intelligence?"
}
```

**Response:**
```json
{
  "answer": "AI refers to computer technologies that enable machines...",
  "sources": [{ "text": "...", "chunk_index": 0 }],
  "doc_id": "76c0d933-..."
}
```

---

## What I learned

- ✅ RAG pipeline end-to-end
- ✅ Vector databases & semantic search
- ✅ Local LLMs with Ollama
- ✅ Async file handling in FastAPI
- ✅ Multi-service project structure
- ✅ Debugging from stack traces
- ✅ Text chunking strategies
- ✅ Pydantic validation schemas

---

*Built by Faker Nour · ENICarthage · Tunisia*