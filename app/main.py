from fastapi import FastAPI
from app.routers import upload, ask
from app.services.retriever import chroma_client
app = FastAPI(
    title="RAG PDF Q&A API",
    description="Upload a PDF, ask questions, get answers grounded in the document.",
    version="1.0.0"
)

app.include_router(upload.router, prefix="/api/v1", tags=["upload"])
app.include_router(ask.router, prefix="/api/v1", tags=["ask"])

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/debug/{doc_id}")
def debug_collection(doc_id: str):
    try:
        collection = chroma_client.get_collection(name=doc_id)
        count = collection.count()
        
        # Get a sample chunk
        sample = collection.get(limit=2, include=["documents", "embeddings", "metadatas"])
        
        return {
            "collection_exists": True,
            "chunk_count": count,
            "sample_texts": [d[:100] for d in sample["documents"]],
            "sample_metadata": sample["metadatas"],
            "embedding_dimensions": len(sample["embeddings"][0]) if sample["embeddings"] else 0
        }
    except Exception as e:
        return {"collection_exists": False, "error": str(e)}