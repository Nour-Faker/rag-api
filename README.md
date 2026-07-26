<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:c084fc,50:818cf8,100:38bdf8&height=200&section=header&text=RAG%20PDF%20Q%26A%20API&fontSize=52&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Upload%20any%20PDF.%20Ask%20anything.%20Get%20grounded%20answers%20with%20sources.&descAlignY=60&descSize=16&descColor=e9d5ff" />

</div>

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-c084fc?style=for-the-badge&logo=fastapi&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-818cf8?style=for-the-badge)
![Ollama](https://img.shields.io/badge/Ollama-7dd3fc?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-a855f7?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python_3.11-f9a8d4?style=for-the-badge&logo=python&logoColor=white)

</div>

---

## What This Is

A production-grade **Retrieval Augmented Generation (RAG)** API built from scratch — not a LangChain wrapper, not a tutorial copy.

Upload any PDF. Ask a question in natural language. Get an answer grounded in your document with exact source citations and similarity scores. Runs **100% locally** — no OpenAI key, no cloud costs, no data leaves your machine.

---

## Architecture

```
                        INDEXING (offline)
┌─────────┐    ┌──────────────┐    ┌─────────────────┐    ┌────────────┐
│   PDF   │───▶│ Text Extract │───▶│ Recursive Chunk │───▶│  Nomic     │
│  Upload │    │   (pypdf)    │    │  (500t / 50t    │    │  Embed     │
└─────────┘    └──────────────┘    │   overlap)      │    │  (Ollama)  │
                                   └─────────────────┘    └─────┬──────┘
                                                                 │
                                                          ┌──────▼──────┐
                                                          │  ChromaDB   │
                                                          │  (cosine)   │
                                                          └─────────────┘

                        QUERYING (per request)
┌──────────┐    ┌──────────────┐    ┌─────────────┐    ┌────────────────┐
│ Question │───▶│  Embed Query │───▶│ Vector Search│───▶│ Cross-Encoder  │
└──────────┘    │  (Ollama)    │    │  top-10      │    │  Reranker      │
                └──────────────┘    └─────────────┘    │  → top-3       │
                                                        └───────┬────────┘
                                                                │
                                                        ┌───────▼────────┐
                                                        │  Ollama LLM    │
                                                        │  (tinyllama)   │
                                                        └───────┬────────┘
                                                                │
                                                        ┌───────▼────────┐
                                                        │ Answer +       │
                                                        │ Sources +      │
                                                        │ Scores         │
                                                        └────────────────┘
```

---

## Why I Built It This Way

Most RAG tutorials use LangChain abstractions that hide what's actually happening. I built every layer manually to understand — and control — the tradeoffs:

**Chunking:** Used `RecursiveCharacterTextSplitter` instead of fixed-size splitting. Fixed-size splits sentences mid-way and destroys context. Recursive splitting respects paragraph → sentence → word boundaries.

**Cosine distance:** ChromaDB defaults to L2 distance. I explicitly set `hnsw:space: cosine` because embedding similarity is angular, not Euclidean. Without this, retrieval produces garbage scores.

**Reranking:** Vector similarity ≠ relevance. I retrieve top-10 by embedding similarity, then pass them through a cross-encoder (`ms-marco-MiniLM-L-6-v2`) that reads query + chunk together and reranks by true relevance. The top-3 go to the LLM.

**Local-first:** Everything runs via Ollama. No external API calls. No rate limits. No cost. Works offline.

---

## Stack

| Layer | Technology | Why |
|---|---|---|
| API framework | FastAPI | async, typed, auto-docs |
| PDF extraction | pypdf | lightweight, no Java dependency |
| Chunking | langchain-text-splitters | recursive splitting respects boundaries |
| Embeddings | nomic-embed-text (Ollama) | free, local, strong quality |
| Vector DB | ChromaDB | persistent, cosine distance, zero infra |
| Reranking | cross-encoder/ms-marco-MiniLM-L-6-v2 | improves precision over raw vector search |
| LLM | tinyllama (Ollama) | free, local, fast on CPU |
| Deployment | Docker + docker-compose | reproducible, one-command run |

---

## Quick Start

### Prerequisites

Install [Ollama](https://ollama.ai) and pull the required models:

```bash
ollama pull nomic-embed-text
ollama pull tinyllama
```

### Run with Docker

```bash
git clone https://github.com/Nour-Faker/rag-api
cd rag-api
docker compose up --build
```

> First build takes ~5 minutes (downloads PyTorch CPU + reranker model).
> Subsequent starts are instant — everything is cached.

API: `http://localhost:8000`
Swagger UI: `http://localhost:8000/docs`

### Run locally (without Docker)

```bash
python -m venv venv
.\venv\Scripts\activate        # Windows
source venv/bin/activate       # Mac/Linux

pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

---

## API Reference

### `POST /api/v1/upload` — Index a PDF

```bash
curl -X POST http://localhost:8000/api/v1/upload \
  -F "file=@your_document.pdf"
```

**Response:**
```json
{
  "doc_id": "ff865a92-06e2-4933-be87-b7ecda3f3275",
  "chunks_stored": 87,
  "filename": "your_document.pdf",
  "message": "Successfully processed your_document.pdf"
}
```

Save the `doc_id` — you need it to query this document.

---

### `POST /api/v1/ask` — Ask a Question

```bash
curl -X POST http://localhost:8000/api/v1/ask \
  -H "Content-Type: application/json" \
  -d '{
    "doc_id": "ff865a92-06e2-4933-be87-b7ecda3f3275",
    "question": "What is the main topic of this document?"
  }'
```

**Response:**
```json
{
  "answer": "According to chunk 3, the document discusses the background and political career of Barack Obama, including his 2008 presidential election victory...",
  "sources": [
    {
      "text": "Il obtient 52,9 % des voix et 365 grands électeurs à l'élection présidentielle de 2008...",
      "chunk_index": 5,
      "similarity": 0.5947,
      "rerank_score": 8.4231,
      "source": "test-rag-api.pdf"
    },
    {
      "text": "Il étudie ensuite pendant trois ans à la faculté de droit de Harvard...",
      "chunk_index": 70,
      "similarity": 0.5909,
      "rerank_score": 6.1823,
      "source": "test-rag-api.pdf"
    }
  ],
  "doc_id": "ff865a92-06e2-4933-be87-b7ecda3f3275"
}
```

---

### `GET /health` — Health Check

```bash
curl http://localhost:8000/health
# {"status": "ok"}
```

---

## Project Structure

```
rag-api/
├── app/
│   ├── routers/
│   │   ├── upload.py        # PDF ingestion endpoint
│   │   └── ask.py           # Q&A endpoint with reranking
│   ├── services/
│   │   ├── pdf.py           # text extraction from PDF
│   │   ├── chunker.py       # recursive character splitting
│   │   ├── embedder.py      # nomic-embed-text via Ollama
│   │   ├── retriever.py     # ChromaDB cosine search
│   │   └── reranker.py      # cross-encoder reranking
│   ├── main.py              # FastAPI app + router registration
│   └── models.py            # Pydantic request/response models
├── Dockerfile               # CPU-optimized, model baked in
├── docker-compose.yml       # app + volume mounts
├── .dockerignore
└── requirements.txt
```

---

## What I Learned Building This

- **Chunking quality beats embedding model choice.** I spent time comparing chunk strategies — the recursive splitter outperformed fixed-size significantly on retrieval precision.
- **ChromaDB's default distance metric is L2, not cosine.** This caused hours of debugging — retrieval scores were in the hundreds instead of 0-1. Explicitly setting `hnsw:space: cosine` fixed it.
- **Reranking changes the order, not just the score.** Chunks with lower vector similarity often rank higher after reranking — because semantic similarity and actual relevance are different things.
- **Docker + local LLMs is a powerful combo.** The whole system runs offline with one command. No API keys, no billing, no rate limits.

---

## What's Next

- [ ] Hybrid retrieval (dense + BM25) for better keyword matching
- [ ] RAGAS evaluation pipeline
- [ ] Multi-document support (query across multiple PDFs)
- [ ] PostgreSQL metadata store (replace in-memory doc tracking)
- [ ] Streaming responses

---

<div align="center">

*Built from scratch during Year 1 CS Engineering at ENICarthage 🌸*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Nour_Faker-818cf8?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/nour-faker-82b691386/)
[![GitHub](https://img.shields.io/badge/GitHub-Nour--Faker-f9a8d4?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Nour-Faker)

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:38bdf8,50:818cf8,100:c084fc&height=100&section=footer"/>

</div>