from sentence_transformers import CrossEncoder
from typing import List, Dict

# Load once at startup — don't reload on every request
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(query: str, chunks: List[Dict], top_n: int = 3) -> List[Dict]:
    if not chunks:
        return []

    # Build pairs of (query, chunk_text) for the cross-encoder
    texts = [chunk["text"] for chunk in chunks]
    pairs = [(query, text) for text in texts]

    # Score each pair — cross-encoder reads both together
    scores = reranker.predict(pairs)

    # Attach reranker score to each chunk
    for chunk, score in zip(chunks, scores):
        chunk["rerank_score"] = round(float(score), 4)

    # Sort by reranker score and return top_n
    reranked = sorted(chunks, key=lambda x: x["rerank_score"], reverse=True)

    print(f"✅ Reranked {len(chunks)} chunks → kept top {top_n}")
    for i, chunk in enumerate(reranked[:top_n]):
        print(f"  Rank {i+1}: rerank_score={chunk['rerank_score']:.4f}, similarity={chunk['similarity']:.4f}")

    return reranked[:top_n]