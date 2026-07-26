FROM python:3.11-slim

WORKDIR /app

# Install CPU-only torch first
RUN pip install --no-cache-dir --timeout=300 \
    torch --index-url https://download.pytorch.org/whl/cpu

# Install all dependencies
RUN pip install --no-cache-dir --timeout=300 \
    fastapi uvicorn chromadb pypdf ollama \
    langchain-text-splitters pydantic python-multipart \
    sentence-transformers

# Download the reranker model at build time
RUN python -c "from sentence_transformers import CrossEncoder; CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')"

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]