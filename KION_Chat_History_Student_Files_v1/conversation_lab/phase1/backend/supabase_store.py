"""1단계: 공개 샘플 문서를 읽는 수업용 코드."""

import os

import httpx
from fastapi import HTTPException


def read_documents(select):
    url = os.getenv("SUPABASE_URL", "").rstrip("/")
    key = os.getenv("SUPABASE_PUBLISHABLE_KEY", "")
    if not url or not key:
        raise HTTPException(500, "Supabase 환경 변수가 없습니다.")
    try:
        response = httpx.get(
            url + "/rest/v1/documents",
            headers={"apikey": key, "Accept-Profile": "llm"},
            params={"select": select, "order": "created_at.desc"},
            timeout=15,
        )
        response.raise_for_status()
    except httpx.HTTPError:
        raise HTTPException(502, "Supabase 문서 읽기에 실패했습니다.")
    return response.json()


def list_documents():
    return read_documents("id,filename,created_at")


def all_document_texts():
    return read_documents("filename,content")
