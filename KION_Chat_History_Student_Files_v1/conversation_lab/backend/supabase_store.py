"""현재 로그인 사용자의 JWT를 Supabase REST API에 전달합니다."""

import os

import httpx
from fastapi import HTTPException


SUPABASE_URL = os.getenv("SUPABASE_URL", "").rstrip("/")
PUBLISHABLE_KEY = os.getenv("SUPABASE_PUBLISHABLE_KEY", "")


def check_settings():
    if not SUPABASE_URL or not PUBLISHABLE_KEY:
        raise HTTPException(status_code=500, detail="Supabase 환경 변수가 없습니다.")


def request_headers(user_token):
    check_settings()
    return {
        "apikey": PUBLISHABLE_KEY,
        # Supabase가 이 사용자 JWT를 검사하고 RLS에 사용합니다.
        "Authorization": "Bearer " + user_token,
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }


def call_database(method, user_token, params=None, body=None):
    url = SUPABASE_URL + "/rest/v1/documents"
    headers = request_headers(user_token)
    # PostgREST는 읽기와 쓰기에서 스키마를 지정하는 헤더가 다릅니다.
    if method == "GET":
        headers["Accept-Profile"] = "llm"
    else:
        headers["Content-Profile"] = "llm"
    try:
        response = httpx.request(
            method,
            url,
            headers=headers,
            params=params,
            json=body,
            timeout=15,
        )
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="DB 연결에 실패했습니다.")

    if response.status_code == 401:
        raise HTTPException(status_code=401, detail="다시 로그인하세요.")
    if response.status_code == 403:
        raise HTTPException(status_code=403, detail="문서 접근 권한이 없습니다.")
    if response.status_code == 409:
        raise HTTPException(status_code=409, detail="같은 이름의 문서가 있습니다.")
    if response.status_code >= 400:
        # 서버 내부 오류 원문을 브라우저에 그대로 노출하지 않습니다.
        raise HTTPException(status_code=502, detail="문서 DB 요청에 실패했습니다.")
    return response.json()


def list_documents(user_token):
    return call_database(
        "GET",
        user_token,
        params={"select": "id,filename,created_at", "order": "created_at.desc"},
    )


def all_document_texts(user_token):
    return call_database(
        "GET",
        user_token,
        params={"select": "filename,content", "order": "created_at.desc"},
    )


def add_document(user_token, user_id, filename, content):
    rows = call_database(
        "POST",
        user_token,
        body={"user_id": user_id, "filename": filename, "content": content},
    )
    return rows[0]
