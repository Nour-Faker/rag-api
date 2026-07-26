from fastapi import APIRouter, HTTPException
import ollama
import os
from app.models import AskRequest, AskResponse, SourceChunk
from app.services.retriever import retrieve_chunks
from app.services.reranker import rerank

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost:11434")
client = ollama.Client(host=f"http://{OLLAMA_HOST}")

def embed_texts(texts):
    # replace ollama.embeddings with client.embeddings
    response = client.embeddings(model="nomic-embed-text", prompt=text)
    
router = APIRouter()

@router.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):

    # 1. Retrieve top 10 candidates
    results = retrieve_chunks(
        doc_id=request.doc_id,
        question=request.question,
        top_k=10,
        score_threshold=0.2  # lower threshold — reranker will filter
    )

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No relevant content found for this question"
        )

    # 2. Rerank — pick best 3 from top 10
    top_results = rerank(
        query=request.question,
        chunks=results,
        top_n=3
    )

    # 3. Build context with rerank scores
    context_parts = []
    for i, r in enumerate(top_results):
        source = r["metadata"].get("source", "unknown")
        idx = r["metadata"].get("chunk_index", i)
        context_parts.append(
            f"[Chunk {idx} | {source}]\n{r['text']}"
        )
    context = "\n\n---\n\n".join(context_parts)

    # 4. Build prompt
    prompt = f"""You are a helpful assistant. Answer the question based ONLY on the context below.
If the answer is not in the context, say "I cannot find this information in the document."
Mention which chunk your answer comes from.

Context:
{context}

Question: {request.question}

Answer:"""

    # 5. Call Ollama
    response = ollama.chat(
        model="tinyllama",
        messages=[{"role": "user", "content": prompt}]
    )
    answer = response["message"]["content"]

    # 6. Return with rerank scores
    return AskResponse(
        answer=answer,
        sources=[
            SourceChunk(
                text=r["text"],
                chunk_index=r["metadata"].get("chunk_index", i),
                similarity=r["similarity"],
                rerank_score=r.get("rerank_score"),
                source=r["metadata"].get("source", "unknown")
            )
            for i, r in enumerate(top_results)
        ],
        doc_id=request.doc_id
    )