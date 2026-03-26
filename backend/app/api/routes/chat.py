from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models import Document
from app.db.session import get_db
from app.rag.retrieval import retrieve_relevant_chunks
from app.rag.prompts import build_rag_prompt
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.ollama import generate_answer

router = APIRouter()

@router.post("/", response_model = ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db),) -> ChatResponse:
    document = db.query(Document).filter(Document.id == request.document_id).first()

    if document is None:
        raise HTTPException(status_code = 404, detail = "Document not found.")
    
    retrieved_chunks = retrieve_relevant_chunks(
        question = request.question,
        document_id = request.document_id,
        db = db,
        top_k = 3,
    )

    prompt = build_rag_prompt(request.question, retrieved_chunks)

    answer = generate_answer(prompt)

    return ChatResponse(answer = answer, retrieved_chunks = retrieved_chunks,)