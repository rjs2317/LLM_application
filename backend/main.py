"""기존 질문 API에 문서 목록과 TXT 업로드 API를 더한 완성 예시."""

from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, UploadFile
from google import genai
from pydantic import BaseModel, Field

from document_store import add_document, list_documents
from retrieval import find_chunks


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR.parent / ".env")
app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")
MAX_FILE_SIZE = 1_000_000  # 수업에서는 TXT 파일을 1 MB까지만 받습니다.


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)


@app.get("/api/documents")
def get_documents():
    # 브라우저 왼쪽 목록에는 문서 내용 대신 이름과 ID만 보냅니다.
    return {"documents": list_documents()}


@app.post("/api/documents")
def upload_document(file: UploadFile):
    # 브라우저가 보낸 파일명에서 폴더 경로를 제거합니다.
    filename = (file.filename or "").replace("\\", "/").split("/")[-1]
    if not filename.lower().endswith(".txt"):
        raise HTTPException(status_code=400, detail="TXT 파일만 올릴 수 있습니다.")

    # 크기를 제한하고 UTF-8 텍스트인지 확인합니다.
    data = file.file.read(MAX_FILE_SIZE + 1)
    if len(data) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="파일은 1 MB 이하여야 합니다.")
    try:
        content = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="UTF-8 TXT 파일을 선택하세요.")
    if not content.strip():
        raise HTTPException(status_code=400, detail="내용이 비어 있습니다.")

    document_id = add_document(filename, content)
    if document_id is None:
        raise HTTPException(status_code=409, detail="같은 이름의 문서가 있습니다.")
    return {"id": document_id, "filename": filename}


@app.post("/api/chat")
def chat(request: ChatRequest):
    chunks = find_chunks(request.question)
    if not chunks:
        return {"answer": "자료에서 관련 내용을 찾지 못했습니다.", "sources": []}

    context = ""
    for chunk in chunks:
        context += "파일: " + chunk["source"] + "\n"
        context += chunk["text"] + "\n\n"

    prompt = "아래 발췌문을 근거로 질문에 답하세요.\n"
    prompt += "발췌문에 답이 없으면 근거가 부족하다고 말하세요.\n\n"
    prompt += "발췌문:\n" + context
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
    return {"answer": interaction.output_text, "sources": sources}
