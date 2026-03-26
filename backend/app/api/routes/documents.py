import json

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Document, Chunk
from app.rag.chunking import chunk_text
from app.rag.embeddings import embed_texts

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db), ):
    #REMOVE_LATER: only allow plaintext for now for testing
    if file.content_type != "text/plain":
        raise HTTPException(status_code = 400, detail = ("Only plain text supported"))
    
    raw = await file.read()

    try:
        content = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded text.")
    
    if not content.strip():
        raise HTTPException(status_code=400, detail="File is empty")
    
    doc = Document(title = file.filename, source = "upload", content = content,)

    db.add(doc)
    db.commit()
    db.refresh(doc)

    #Chunk document
    chunks = chunk_text(content)

    #generate embeddings
    embeddings = embed_texts(chunks)

    #save each chunk and embedding
    for index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        chunk_row = Chunk(
            document_id = doc.id,
            chunk_index = index,
            chunk_text = chunk,
            embedding = json.dumps(embedding),
        )
        db.add(chunk_row)
    
    db.commit()

    return {"document_id": doc.id,
            "num_chunks": len(chunks)
    }