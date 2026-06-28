from fastapi import APIRouter, HTTPException
import ollama
from app.models import AskRequest, AskResponse, SourceChunk
from app.services.retriever import retrieve_chunks

router = APIRouter()

@router.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    # 1. retrieve relevant chunks from ChromaDB
    chunks = retrieve_chunks(request.doc_id, request.question)

    if not chunks:
        raise HTTPException(status_code=404, detail="No content found for this document")

    # 2. build context from chunks
    context = "\n\n".join(chunks)

    # 3. build prompt
    prompt = f"""You are a helpful assistant. Answer the question based ONLY on the context below.
If the answer is not in the context, say "I cannot find this information in the document."

Context:
{context}

Question: {request.question}

Answer:"""

    # 4. call local LLM via Ollama
    response = ollama.chat(
        model="tinyllama",
        messages=[{"role": "user", "content": prompt}]
    )
    answer = response["message"]["content"]

    # 5. return answer + sources
    return AskResponse(
        answer=answer,
        sources=[SourceChunk(text=chunk, chunk_index=i) for i, chunk in enumerate(chunks)],
        doc_id=request.doc_id
    )