"""1단계: 공개 URL의 위험을 확인하기 위한 샘플 문서 챗봇."""

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from google import genai
from pydantic import BaseModel, Field

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from retrieval import find_chunks  # noqa: E402
from supabase_store import all_document_texts, list_documents  # noqa: E402

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)


@app.get("/api/documents")
def get_documents():
    return {"documents": list_documents()}


@app.post("/api/chat")
def chat(request: ChatRequest):
    documents = all_document_texts()
    chunks = find_chunks(request.question, documents)
    if not chunks:
        return {"answer": "공개 샘플 자료에서 찾지 못했습니다.", "sources": []}

    context = ""
    sources = []
    for chunk in chunks:
        context += "파일: " + chunk["source"] + "\n"
        context += chunk["text"] + "\n\n"
        if chunk["source"] not in sources:
            sources.append(chunk["source"])

    prompt = "아래 발췌문만 근거로 답하세요. 없으면 근거가 부족하다고 말하세요.\n"
    prompt += "발췌문:\n" + context + "\n질문: " + request.question
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    answer = client.interactions.create(
        model="gemini-3.5-flash-lite", input=prompt
    )
    return {"answer": answer.output_text, "sources": sources}
