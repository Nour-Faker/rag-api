from pydantic import BaseModel
from typing import List, Optional

class UploadResponse(BaseModel):
    doc_id:str
    chunks_stored:int
    message:str

class AskRequest(BaseModel):
    doc_id:str
    question:str

class SourceChunk(BaseModel):
    text: str
    chunk_index: int  # ✅

class AskResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]
    doc_id: str  # ✅
