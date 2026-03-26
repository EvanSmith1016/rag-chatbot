from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime, timezone

from app.db.base import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key= True, index = True)
    title = Column(String(255), nullable = True)
    content = Column(Text, nullable = False)

    source = Column(String(255), nullable = False)
    created_at = Column(DateTime(timezone = True), default = lambda: datetime.now(timezone.utc))

class Chunk(Base): 
    __tablename__ = "chunks"

    id = Column(Integer, primary_key= True, index = True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable = False)
    chunk_index = Column(Integer, nullable = False)
    chunk_text = Column(Text, nullable = False)
    embedding = Column(Text, nullable = False)
                