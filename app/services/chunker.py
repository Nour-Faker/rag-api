from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = splitter.split_text(text)
    # Filter out empty or very short chunks
    return [c.strip() for c in chunks if len(c.strip()) > 50]