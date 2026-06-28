import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf import extract_text
from app.services.chunker import chunk_text
from app.services.retriever import store_chunks
from app.models import UploadResponse

router = APIRouter()

@router.post("/upload", response_model=UploadResponse, status_code=201)
async def upload_pdf(file: UploadFile = File(...)):
    # 1. validate file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    
    # 2. extract text from PDF
    try:
        text = await extract_text(file)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    print(f"DEBUG: extracted text length = {len(text)}") 
    # 3. chunk the text
    chunks = chunk_text(text)
    print(f"DEBUG: chunks = {len(chunks)}")
    # 4. store chunks in ChromaDB
    doc_id = str(uuid.uuid4())  # unique ID for this document
    stored = store_chunks(doc_id, chunks)
    
    return UploadResponse(
        doc_id=doc_id,
        chunks_stored=stored,
        message=f"Successfully processed {file.filename}"
    )