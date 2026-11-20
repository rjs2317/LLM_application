# 브라우저에서 TXT 문서 추가하기 — 강사용 완성 예시

이 자료는 11월 19일 오후 실습의 **완성 예시**입니다. 학생들은 자신의 `LLM_Application` 프로젝트에서 한 단계씩 작성합니다. 기존에 질문 기능을 수정한 학생은 `backend/main.py`, `backend/retrieval.py`를 통째로 덮어쓰지 말고 새 코드 부분을 비교해 합칩니다.

## 먼저 준비하기

1. 앞의 SQLite 실습으로 `LLM_Application/sqlite_lab/documents.db`를 만듭니다. DB가 없어도 첫 API 호출 때 빈 DB가 만들어지지만, 세 문서를 먼저 가져온 상태가 수업에 더 좋습니다.
2. 프로젝트 루트의 `.gitignore`에 `sqlite_lab/*.db`를 추가합니다.
3. 프로젝트 루트 터미널에서 `.\.venv\Scripts\python.exe -m pip install python-multipart`를 실행합니다. 파일 업로드를 받는 FastAPI 의존성입니다.

## 백엔드 파일

- 새 파일: `backend/document_store.py`를 복사합니다.
- 기존 파일 수정: `backend/retrieval.py`의 `load_chunks()`가 `backend/data` 대신 SQLite 문서를 읽도록 바꿉니다. `make_words()`와 `find_chunks()`는 지난 실습 코드를 유지해도 됩니다.
- 기존 파일 수정: `backend/main.py`에 `/api/documents` GET, POST를 추가합니다. `chat()`는 기존 코드를 유지해도 됩니다.

프로젝트 루트에서 백엔드를 실행합니다.

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --app-dir backend --reload
```

`http://127.0.0.1:8000/api/docs`에서 GET `/api/documents`를 먼저 실행하여 기존 세 문서가 목록에 있는지 확인합니다.

## 프론트엔드 파일

- 새 파일 두 개: `frontend/src/DocumentSources.jsx`, `frontend/src/DocumentSources.css`.
- 기존 `frontend/src/App.jsx` 맨 위에 `import DocumentSources from './DocumentSources'`를 추가합니다.
- `<header className="header">...</header>` 바로 뒤에 `<DocumentSources />`를 추가합니다.
- 기존 `frontend/src/App.css` 끝에 아래 CSS를 추가합니다.

```css
.app {
  width: min(1180px, calc(100% - 32px));
  display: grid;
  grid-template-columns: 270px minmax(0, 1fr);
  grid-template-rows: auto 1fr auto;
  gap: 0 18px;
}
.header { grid-column: 1 / -1; }
.chat { grid-column: 2; grid-row: 2; }
.composer { grid-column: 2; grid-row: 3; }
@media (max-width: 700px) {
  .app { grid-template-columns: 1fr; grid-template-rows: auto auto 1fr auto; }
  .header, .sources, .chat, .composer { grid-column: 1; }
  .sources { grid-row: 2; margin-bottom: 16px; }
  .chat { grid-row: 3; }
  .composer { grid-row: 4; }
}
```

프론트엔드 터미널에서는 `cd frontend` 다음 `npm run dev`를 실행합니다. Vite의 `/api` 프록시가 백엔드 포트 8000을 가리켜야 합니다.

## 확인 순서

1. 브라우저 왼쪽에 기존 TXT 세 개가 보이는지 확인합니다.
2. `sample_uploads/uiux_기초.txt`를 선택해 추가합니다. 목록에 즉시 나타나야 합니다.
3. DB Browser for SQLite에서 같은 `sqlite_lab/documents.db`를 새로고침하여 행이 늘었는지 확인합니다.
4. 새 문서 내용으로 질문해 답변의 출처 파일명이 새 문서인지 확인합니다.
5. 같은 이름 다시 업로드, PDF 선택, 빈 TXT를 시도하여 오류 메시지를 확인합니다.

이 실습은 **로컬 개발 환경**에서 합니다. SQLite 파일은 Vercel의 지속 저장소가 아니며, 공개 서비스로 업로드 기능을 배포하려면 Supabase 같은 지속 저장소와 사용자 인증·접근 규칙을 설계해야 합니다.
