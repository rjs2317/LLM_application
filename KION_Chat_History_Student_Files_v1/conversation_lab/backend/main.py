"""기존 FastAPI 앱의 Supabase 연결 완성 예시."""

from pathlib import Path
from uuid import UUID

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, UploadFile
from google import genai
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR.parent / ".env")

from retrieval import find_chunks  # noqa: E402
from supabase_store import add_document, all_document_texts, list_documents  # noqa: E402
from auth_guard import require_approved  # noqa: E402
from chat_store import (  # noqa: E402
    create_session, get_session, list_sessions, list_turns, save_turn,
)


app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")
MAX_FILE_SIZE = 1_000_000


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)
    session_id: UUID


class CreateChatRequest(BaseModel):
    title: str = Field(min_length=1, max_length=80)


@app.get("/api/documents")
def get_documents(authorization: str = Header(default="")):
    token, user_id = require_approved(authorization)
    return {"documents": list_documents(token)}


@app.post("/api/documents")
def upload_document(file: UploadFile, authorization: str = Header(default="")):
    token, user_id = require_approved(authorization)
    filename = (file.filename or "").replace("\\", "/").split("/")[-1]
    if not filename.lower().endswith(".txt"):
        raise HTTPException(status_code=400, detail="TXT 파일만 올릴 수 있습니다.")
    if len(filename) > 200:
        raise HTTPException(status_code=400, detail="파일명이 너무 깁니다.")

    data = file.file.read(MAX_FILE_SIZE + 1)
    if len(data) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="파일은 1 MB 이하여야 합니다.")
    try:
        content = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="UTF-8 TXT 파일을 선택하세요.")
    if not content.strip():
        raise HTTPException(status_code=400, detail="내용이 비어 있습니다.")

    document = add_document(token, user_id, filename, content)
    return {"id": document["id"], "filename": document["filename"]}


@app.get("/api/chat-sessions")
def get_chat_sessions(authorization: str = Header(default="")):
    token, user_id = require_approved(authorization)
    return {"sessions": list_sessions(token)}


@app.post("/api/chat-sessions")
def new_chat_session(
    request: CreateChatRequest, authorization: str = Header(default="")
):
    token, user_id = require_approved(authorization)
    session = create_session(token, user_id, request.title)
    return {"session": session}


@app.get("/api/chat-sessions/{session_id}/turns")
def get_chat_turns(session_id: UUID, authorization: str = Header(default="")):
    token, user_id = require_approved(authorization)
    get_session(token, str(session_id))  # 다른 사용자의 채팅 ID는 조회되지 않습니다.
    return {"turns": list_turns(token, str(session_id))}


@app.post("/api/chat")
def chat(request: ChatRequest, authorization: str = Header(default="")):
    token, user_id = require_approved(authorization)
    session_id = str(request.session_id)
    get_session(token, session_id)  # Gemini 호출 전에 채팅방 소유권을 확인합니다.
    turns = list_turns(token, session_id)
    recent_turns = turns[-5:]

    # RLS가 허용한 현재 사용자의 문서만 가져옵니다.
    documents = all_document_texts(token)
    chunks = find_chunks(request.question, documents)

    # "그 내용을 더 설명해줘"처럼 앞 질문을 가리키면 앞 질문의 근거를 다시 찾습니다.
    follow_up_words = ("그 ", "그것", "이전 ", "위 ", "방금 ")
    if recent_turns and request.question.strip().startswith(follow_up_words):
        chunks = find_chunks(recent_turns[-1]["question"], documents)

    if not chunks:
        answer = "내 문서에서 관련 내용을 찾지 못했습니다."
        saved = save_turn(token, session_id, request.question, answer, [])
        return {"answer": answer, "sources": [], "turn": saved}

    context = ""
    for chunk in chunks:
        context += "파일: " + chunk["source"] + "\n"
        context += chunk["text"] + "\n\n"

    prompt = "아래 발췌문을 근거로 질문에 답하세요.\n"
    prompt += "이전 대화는 문맥을 이해할 때만 사용하세요.\n"
    prompt += "발췌문에 답이 없으면 근거가 부족하다고 말하세요.\n\n"
    prompt += "발췌문:\n" + context
    prompt += "최근 대화:\n"
    for turn in recent_turns:
        prompt += "사용자: " + turn["question"] + "\n"
        prompt += "챗봇: " + turn["answer"] + "\n"
    prompt += "질문: " + request.question

    client = genai.Client()
    interaction = client.interactions.create(
        model="gemini-3.5-flash-lite", input=prompt
    )

    sources = []
    for chunk in chunks:
        name = chunk["source"]
        if name not in sources:
            sources.append(name)
    answer = interaction.output_text or "답변을 생성하지 못했습니다. 다시 질문해 주세요."
    saved = save_turn(token, session_id, request.question, answer, sources)
    return {"answer": answer, "sources": sources, "turn": saved}
