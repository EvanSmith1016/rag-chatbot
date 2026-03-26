from fastapi import FastAPI
from app.db.init_db import init_db
from app.api.routes import documents, chat

# Initialize DB tables immediately
init_db()

# Create FastAPI app
app = FastAPI(
    title="RAG Chatbot Backend",
    description="Backend API for a Retrieval Augmented chatbot",
    version="0.1.0"
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(documents.router, prefix = "/documents", tags = ["documents"])
app.include_router(chat.router, prefix = "/chat", tags = ["chat"])