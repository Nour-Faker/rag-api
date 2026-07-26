import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf import extract_text
from app.services.chunker import chunk_text
from app.services.retriever import store_chunks
from app.models import UploadResponse

router = APIRouter()

@router.post("/upload", response_model=UploadResponse, status_code=201)
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    try:
        text = await extract_text(file)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    print(f"✅ Extracted {len(text)} characters from {file.filename}")

    chunks = chunk_text(text)
    print(f"✅ Created {len(chunks)} chunks")

    doc_id = str(uuid.uuid4())

    # ← pass filename here — this is what was missing
    stored = store_chunks(doc_id, chunks, source_filename=file.filename)

    return UploadResponse(
        doc_id=doc_id,
        chunks_stored=stored,
        filename=file.filename,
        message=f"Successfully processed {file.filename}"
    )