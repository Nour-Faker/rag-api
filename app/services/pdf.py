import pypdf
import io
from fastapi import UploadFile

async def extract_text(file: UploadFile) -> str:
    content = await file.read()
    pdf = pypdf.PdfReader(io.BytesIO(content))
    
    pages = []
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            pages.append(text)
    
    if not pages:
        raise ValueError("Could not extract text from PDF. It may be scanned or image-based.")
    
    return "\n\n".join(pages)