from fastapi import FastAPI, UploadFile, File
import shutil

from services.pdf_service import extract_text
from services.chunking import chunk_text
from services.embedding_service import get_embedding
from services.db import insert_document
from services.rag_service import ask_question
from pydantic import BaseModel

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text(file_path)
    chunks = chunk_text(text)

    for chunk in chunks:
        embedding = get_embedding(chunk)
        insert_document(chunk, embedding)

    return {"message": "PDF processed successfully"}


@app.post("/ask")
async def ask(req: QuestionRequest):
    answer = ask_question(req.question)
    return {"answer": answer}