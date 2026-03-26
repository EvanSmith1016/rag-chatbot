import json
import numpy as np
from sqlalchemy.orm import Session

from app.db.models import Chunk
from app.rag.embeddings import embed_text

def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    denominator = np.linalg.norm(vec_a) * np.linalg.norm(vec_b)
    if denominator == 0:
        return 0.0
    return float(np.dot(vec_a, vec_b) / denominator)

def retrieve_relevant_chunks(
        question: str,
        document_id: id,
        db: Session,
        top_k: int = 3,
) -> list[str]:

    #embed user's question
    question_embedding = np.array(embed_text(question))

    #load all chunks for the document
    chunk_rows = db.query(Chunk).filter(Chunk.document_id == document_id).all()

    scored_chunks = []

    for chunk in chunk_rows:
        chunk_embedding = np.array(json.loads(chunk.embedding))
        score = cosine_similarity(question_embedding, chunk_embedding)
        scored_chunks.append((score, chunk.chunk_text))

    #sort by highest simllarity first
    scored_chunks.sort(key = lambda x: x[0], reverse = True)

    #return top-k chunks texts only
    top_chunks = [chunk_text for _, chunk_text in scored_chunks[:top_k]]

    return top_chunks
