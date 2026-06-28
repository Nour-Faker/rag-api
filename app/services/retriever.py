import chromadb
from typing import List
from app.services.embedder import embed_texts, embed_query

chroma_client = chromadb.PersistentClient(path="./chroma_db")

def get_collection(doc_id: str):
    return chroma_client.get_or_create_collection(name=doc_id)

def store_chunks(doc_id: str, chunks: List[str]):
    collection = get_collection(doc_id)
    embeddings = embed_texts(chunks)
    print(f"DEBUG: chunks={len(chunks)}, embeddings={len(embeddings)}")  # ADD THIS
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
    )
    return len(chunks)

def retrieve_chunks(doc_id: str, question: str, top_k: int = 3):
    collection = get_collection(doc_id)
    query_embedding = embed_query(question)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results["documents"][0]