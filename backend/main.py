from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from google import genai
from pydantic import BaseModel, Field
from retrieval import find_chunks


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR.parent / ".env")
app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)


@app.post("/api/chat")
def chat(request: ChatRequest):
    #document = (BASE_DIR / "data" / "git_기초.txt").read_text(encoding="utf-8")

    chunks = find_chunks(request.question)
    if not chunks:
        return{
            "answer":"자료에서 관련 내용을 찾지 못했습니다.",
            "sources":[],
        }

    context = ""
    for chunk in chunks:
        context += "파일: "+chunk["source"] + "\n"
        context += chunk["text"] + "\n\n"

    #prompt = "아래 발췌문을 근거로 질문에 답하세요.\n"
    #prompt += "답이 없으면 근거가 부족하다고 말하세요.\n\n"
    #prompt += "발췌문:\n" + context
    #prompt += "질문: " + request.question

    prompt = f"""아래 자료를 바탕으로 질문에 답하세요.
자료에 없으면 찾을 수 없다고 말하세요.

자료:
{document}

질문: {request.question}"""

    client = genai.Client()
    interaction = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=prompt,
    )
    return {"answer": interaction.output_text}
