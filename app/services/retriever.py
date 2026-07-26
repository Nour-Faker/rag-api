import chromadb
from typing import List, Dict
from app.services.embedder import embed_texts, embed_query

chroma_client = chromadb.PersistentClient(path="./chroma_db")

def get_collection(doc_id: str):
    # Force cosine distance — critical for embedding similarity
    return chroma_client.get_or_create_collection(
        name=doc_id,
        metadata={"hnsw:space": "cosine"}
    )

def store_chunks(doc_id: str, chunks: List[str], source_filename: str = ""):
    collection = get_collection(doc_id)
    embeddings = embed_texts(chunks)

    metadatas = [
        {
            "source": source_filename,
            "chunk_index": i,
            "doc_id": doc_id,
        }
        for i, chunk in enumerate(chunks)
    ]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=[f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
    )
    print(f"✅ Stored {len(chunks)} chunks for doc_id={doc_id}")
    return len(chunks)

def retrieve_chunks(
    doc_id: str,
    question: str,
    top_k: int = 10,
    score_threshold: float = 0.3
) -> List[Dict]:
    collection = get_collection(doc_id)
    query_embedding = embed_query(question)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    chunks = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]


    filtered = []
    for chunk, meta, distance in zip(chunks, metadatas, distances):
        similarity = 1 - distance  # correct for cosine distance
        if similarity >= score_threshold:
            filtered.append({
                "text": chunk,
                "metadata": meta,
                "similarity": round(similarity, 4)
            })

    filtered.sort(key=lambda x: x["similarity"], reverse=True)
    print(f"✅ Retrieved {len(filtered)}/{top_k} chunks above threshold")
    return filtered