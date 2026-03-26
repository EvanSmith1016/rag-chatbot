def build_rag_prompt(question: str, chunks: list[str]) -> str:
    context = "\n\n".join(chunks)

    prompt = f"""
    
    You are a helpful assistant answering questions about a docuement.
    
    Use only the context below to answer the question.
    If the answer is not in the context, say you do not know.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    return prompt.strip()