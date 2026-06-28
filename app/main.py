from fastapi import FastAPI
from app.routers import upload, ask

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