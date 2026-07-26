import os
import ollama
from typing import List

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost:11434")
client = ollama.Client(host=f"http://{OLLAMA_HOST}")

def embed_texts(texts):
    # replace ollama.embeddings with client.embeddings
    response = client.embeddings(model="nomic-embed-text", prompt=text)

def embed_texts(texts: List[str]) -> List[List[float]]:
    embeddings = []
    batch_size = 10

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        for text in batch:
            response = ollama.embeddings(
                model="nomic-embed-text",
                prompt=text
            )
            # Handle both old and new ollama response formats
            if hasattr(response, 'embedding'):
                emb = response.embedding
            elif isinstance(response, dict):
                emb = response["embedding"]
            else:
                emb = list(response.embedding)
            
            embeddings.append(emb)
        print(f"✅ Embedded {min(i+batch_size, len(texts))}/{len(texts)} chunks")

    return embeddings

def embed_query(text: str) -> List[float]:
    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=text
    )
    if hasattr(response, 'embedding'):
        return list(response.embedding)
    elif isinstance(response, dict):
        return response["embedding"]
    return list(response.embedding)