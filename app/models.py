from pydantic import BaseModel
from typing import List, Optional

class AskRequest(BaseModel):
    doc_id: str
    question: str

class SourceChunk(BaseModel):
    text: str
    chunk_index: int
    similarity: Optional[float] = None
    source: Optional[str] = None

class AskResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]
    doc_id: str

class UploadResponse(BaseModel):
    doc_id: str
    chunks_stored: int
    filename: str
    message: str