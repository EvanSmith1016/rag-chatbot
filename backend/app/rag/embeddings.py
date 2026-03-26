from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text: str) -> list[float]:
    embedding = model.encode(text)
    return embedding.tolist()

def embed_texts(texts: list[str]) -> list[list[float]]:
    embeddings = model.encode(texts)
    return [e.tolist() for e in embeddings]