"""Supabase 로그인 토큰과 관리자 승인 여부를 서버에서 확인합니다."""

import os

import httpx
from fastapi import HTTPException


def require_approved(authorization):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    token = authorization[7:].strip()
    if not token:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")

    url = os.getenv("SUPABASE_URL", "").rstrip("/")
    key = os.getenv("SUPABASE_PUBLISHABLE_KEY", "")
    if not url or not key:
        raise HTTPException(status_code=500, detail="Supabase 설정이 없습니다.")
    headers = {"apikey": key, "Authorization": "Bearer " + token}

    try:
        # Supabase Auth가 토큰의 서명과 만료를 검증합니다.
        user_response = httpx.get(url + "/auth/v1/user", headers=headers, timeout=10)
        if user_response.status_code != 200:
            raise HTTPException(status_code=401, detail="다시 로그인하세요.")
        user_id = user_response.json()["id"]

        # 사용자 JWT로 조회하면 RLS가 자기 승인 행만 반환합니다.
        approval_response = httpx.get(
            url + "/rest/v1/approved_users",
            headers={**headers, "Accept-Profile": "llm"},
            params={"select": "user_id", "user_id": "eq." + user_id},
            timeout=10,
        )
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="Supabase 연결에 실패했습니다.")
    if approval_response.status_code != 200:
        raise HTTPException(status_code=502, detail="승인 상태를 확인하지 못했습니다.")
    if not approval_response.json():
        raise HTTPException(status_code=403, detail="관리자 승인 대기 중입니다.")
    return token, user_id
