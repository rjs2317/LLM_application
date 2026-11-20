from fastapi import FastAPI
from pydantic import BaseModel
from chat_service import answer_question

app = FastAPI()

class ChatRequest(BaseModel):
    question: str

@app.post("/api/chat")
def chat(request: ChatRequest):
    return {"answer": answer_question(request.question)}