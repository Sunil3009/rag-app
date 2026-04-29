from services.embedding_service import get_embedding
from services.db import search_similar
import requests

def ask_question(question: str):
    query_embedding = get_embedding(question)
    docs = search_similar(query_embedding)

    context = "\n".join(docs)

    prompt = f"""
Answer the question based on the context below.If not use your general knowledge to answer the question

Context:
{context}

Question:
{question}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]