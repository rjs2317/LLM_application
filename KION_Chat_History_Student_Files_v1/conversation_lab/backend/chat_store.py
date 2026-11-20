"""로그인 사용자의 채팅방과 질문·답변을 Supabase에 저장합니다."""

import os

import httpx
from fastapi import HTTPException


SUPABASE_URL = os.getenv("SUPABASE_URL", "").rstrip("/")
PUBLISHABLE_KEY = os.getenv("SUPABASE_PUBLISHABLE_KEY", "")


def request_table(method, table, token, params=None, body=None):
    if not SUPABASE_URL or not PUBLISHABLE_KEY:
        raise HTTPException(500, "Supabase 설정이 없습니다.")

    # 테이블 이름은 아래 함수에서 고정된 값만 전달합니다.
    url = SUPABASE_URL + "/rest/v1/" + table
    headers = {
        "apikey": PUBLISHABLE_KEY,
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }
    if method == "GET":
        headers["Accept-Profile"] = "llm"
    else:
        headers["Content-Profile"] = "llm"

    try:
        response = httpx.request(
            method, url, headers=headers, params=params, json=body, timeout=15
        )
    except httpx.RequestError:
        raise HTTPException(502, "채팅 DB에 연결하지 못했습니다.")

    if response.status_code == 401:
        raise HTTPException(401, "다시 로그인하세요.")
    if response.status_code == 403:
        raise HTTPException(403, "채팅 접근 권한이 없습니다.")
    if response.status_code >= 400:
        raise HTTPException(502, "채팅 DB 요청에 실패했습니다.")
    return response.json()


def list_sessions(token):
    return request_table(
        "GET", "chat_sessions", token,
        params={"select": "id,title,created_at", "order": "created_at.desc"},
    )


def create_session(token, user_id, title):
    rows = request_table(
        "POST", "chat_sessions", token,
        body={"user_id": user_id, "title": title},
    )
    return rows[0]


def get_session(token, session_id):
    rows = request_table(
        "GET", "chat_sessions", token,
        params={"select": "id,title", "id": "eq." + session_id},
    )
    if not rows:
        raise HTTPException(404, "채팅을 찾지 못했습니다.")
    return rows[0]


def list_turns(token, session_id):
    return request_table(
        "GET", "chat_turns", token,
        params={
            "select": "id,question,answer,sources,created_at",
            "session_id": "eq." + session_id,
            "order": "created_at.asc,id.asc",
        },
    )


def save_turn(token, session_id, question, answer, sources):
    rows = request_table(
        "POST", "chat_turns", token,
        body={
            "session_id": session_id,
            "question": question,
            "answer": answer,
            "sources": sources,
        },
    )
    return rows[0]
