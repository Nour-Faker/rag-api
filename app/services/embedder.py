import ollama
from typing import List

def embed_texts(texts: List[str]) -> List[List[float]]:
    embeddings = []
    for text in texts:
        response = ollama.embeddings(
            model="nomic-embed-text",
            prompt=text
        )
        embeddings.append(response.embedding)
    return embeddings

def embed_query(text: str) -> List[float]:
    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=text
    )
    return response.embedding