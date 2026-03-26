from ollama import chat

def generate_answer(prompt: str, model: str = "llama3") -> str:
    response = chat(
        model = model,
        messages = [
            {
                "role": "user", "content": prompt,
            }
        ],
    )
    
    return response["message"]["content"]