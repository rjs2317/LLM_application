# KION LABS · 대화 저장과 독립 채팅 확장 실습

이 폴더는 기존 승인 사용자 문서 챗봇 실습 파일을 포함한 **확장판**입니다. 기존 `LLM_Application`을 직접 바꾼 결과가 아니므로, 아래 파일을 학생 프로젝트에 비교·반영합니다.

## 3단계: 대화 저장과 독립 채팅 (이번 추가 수업)

1. 먼저 아래 1·2단계까지 완료한 프로젝트에서 회원가입·승인·TXT 질문이 되는지 확인합니다.
2. 본인 Supabase 프로젝트의 SQL Editor에서 `supabase/04_chat_history.sql` 전체를 실행합니다. `llm.chat_sessions`와 `llm.chat_turns`가 만들어지고 RLS가 켜집니다. 앞 단계의 `02_secure.sql`을 이미 적용했어야 합니다.
3. 프로젝트의 `backend/main.py`를 이 폴더의 코드와 비교해 반영하고, `backend/chat_store.py`를 새로 추가합니다. 기존 `auth_guard.py`, `supabase_store.py`, `retrieval.py`는 유지합니다.
4. 프로젝트의 `frontend/src/App.jsx`, `App.css`를 이 폴더의 파일과 비교해 반영합니다. 기존 `DocumentSources.jsx`, `DocumentSources.css`, `supabaseClient.js`는 유지합니다.
5. 로그인 후 질문을 하나 입력합니다. 이때 새 채팅방이 만들어지고 질문·답변 한 쌍이 DB에 저장됩니다. Supabase Table Editor에서 `llm.chat_sessions`, `llm.chat_turns`를 확인합니다.
6. 페이지를 새로고침해 대화가 복원되는지 확인합니다. 이어서 “그 내용을 더 설명해줘”라고 질문해 문맥이 연결되는지 확인합니다.
7. `+ 새 채팅`을 누른 뒤 다른 주제로 질문합니다. 왼쪽 목록에서 이전 채팅과 새 채팅을 오가며 각 대화가 따로 표시되는지 확인합니다.
8. 다른 승인 계정으로 로그인해 이전 계정의 채팅 목록과 대화가 보이지 않는지 확인합니다. 타인 채팅 ID로 직접 API를 호출하면 404가 나와야 합니다.
9. Git 커밋·푸시 후 Vercel에서 새 배포를 확인합니다. 새 환경 변수는 필요하지 않습니다.

**개념:** 로그인 상태는 Supabase Auth 세션이고, 대화 묶음은 `chat_sessions`의 한 행입니다. 브라우저 `sessionStorage`에는 선택한 채팅 ID만 넣습니다. 대화 본문은 Supabase DB에 보관합니다. 이전 질문·답변 최대 5쌍을 Gemini 요청에 포함하므로 새로고침 뒤에도 이전 문맥을 사용할 수 있습니다. 질문과 답변을 한 행에 저장하는 이번 실습은 단순한 수업용 구조입니다.

**시간이 남으면:** PDF와 DOCX는 텍스트를 추출한 뒤 기존 TXT와 같은 `documents.content`에 넣는 흐름을 설명합니다. 별도 파일 처리·크기 제한·오류 처리가 필요하므로 이 자료에는 업로드 코드가 포함되어 있지 않습니다.

이 폴더는 **기존 `LLM_Application`을 수정할 때 비교·복사하는 수업 자료**입니다. 실제 키는 들어 있지 않습니다. 학생마다 **본인 Supabase 프로젝트**의 URL과 publishable key를 사용합니다.

교안 14페이지의 `read_documents` 코드는 REST 요청을 설명하기 위해 **완성 파일에서 일부만 발췌**한 것입니다. 그 코드로 `phase1/backend/supabase_store.py` 전체를 덮어쓰지 않습니다. 실습 파일에는 환경 변수 확인, 요청 오류 처리, 문서 목록과 본문을 읽는 함수까지 들어 있습니다.

수업 중 GET·POST와 RLS를 설명할 때는 프로젝트 루트의 `수업_설명_GET_POST_RLS.txt`를 사용합니다.

## 1단계: 공개 시연 (오전)

1. 본인 Supabase SQL Editor에서 `create schema if not exists llm;`을 먼저 실행합니다.
2. Dashboard의 **Project Settings → Data API**(화면에 따라 **Integrations → Data API → Settings**)에서 **Exposed schemas**에 `llm`을 추가하고 저장합니다. `public`을 삭제할 필요는 없습니다. `llm` 스키마는 테이블을 구분할 뿐, API 노출을 자동으로 막지는 않습니다.
3. SQL Editor에서 `supabase/01_public_demo.sql` 전체를 실행합니다. 앞에서 실행한 `create schema if not exists llm`은 다시 실행해도 됩니다.
4. Table Editor에서 스키마를 `llm`으로 바꾼 뒤 `documents`에 공개 샘플 TXT 내용을 두 행 추가합니다. `user_id`는 비웁니다. 개인 정보는 넣지 않습니다.
5. 기존 프로젝트의 `backend/main.py`, `backend/supabase_store.py`를 이 자료의 `phase1/backend/` 파일과 비교 후 반영합니다. `backend/retrieval.py`는 이 자료의 최상위 `backend/retrieval.py`를 사용합니다.
6. 기존 프로젝트의 `frontend/src/App.jsx`, `DocumentSources.jsx`, 관련 CSS를 `phase1/frontend/src/`와 비교 후 반영합니다.
7. 프로젝트 루트 `.env`에 `SUPABASE_URL`, `SUPABASE_PUBLISHABLE_KEY`, `GEMINI_API_KEY`를 넣습니다. `.env`가 `.gitignore`에 있어야 합니다.
8. 기존 `requirements.txt`에 `httpx`, `python-multipart`가 있는지 확인합니다. 없다면 추가합니다.
9. 로컬 질문 결과와 출처를 확인한 뒤 Git에 커밋·푸시하고 Vercel에서 배포합니다.

**중요:** 1단계는 일부러 인증 없이 공개한 수업 시연입니다. 같은 날 2단계까지 마쳐야 합니다. 질문마다 서버의 Gemini 키를 사용하므로 공개 URL을 널리 공유하지 않습니다.

## 2단계: 승인 사용자만 접근 (오후)

1. Supabase `Authentication → Providers → Email`을 켜고 `Confirm Email`을 끕니다. `Allow new users to sign up`을 켭니다. Confirm Email을 끄면 이메일 소유 여부는 확인되지 않습니다.
2. SQL Editor에서 `supabase/02_secure.sql`을 실행합니다. `llm.documents`의 공개 읽기 정책이 제거됩니다. 이때 1단계 샘플 행은 `user_id`가 없으므로 앱에서 더 이상 보이지 않는 것이 정상입니다.
3. 기존 프로젝트의 `backend/main.py`, `backend/supabase_store.py`, 새 `backend/auth_guard.py`와 `frontend/src/App.jsx`, `DocumentSources.jsx`, `supabaseClient.js`를 이 폴더의 같은 위치 파일과 비교 후 반영합니다. 기존 `backend/retrieval.py`도 이 자료와 비교합니다.
4. 프로젝트 루트 `.env`에 Supabase와 Gemini 값을 유지합니다. `frontend/.env.local`에는 **publishable key만** 넣습니다. 둘 다 Git에서 제외합니다. 프론트의 Supabase 클라이언트는 `db: { schema: 'llm' }`, Python REST의 GET은 `Accept-Profile: llm`, POST는 `Content-Profile: llm`을 사용합니다.
5. `frontend`에서 `npm install @supabase/supabase-js`를 실행합니다.
6. 앱에서 본인 이메일과 비밀번호로 가입합니다. Supabase `Authentication → Users`에서 새 user ID를 복사합니다.
7. **프로젝트 소유자만** SQL Editor에서 `supabase/03_approve_user_example.sql`의 예시 UUID를 실제 ID로 바꿔 실행합니다. 승인 테이블에는 사용자가 직접 쓰지 못합니다.
8. 앱에서 로그인 → `승인 상태 새로고침` → 본인 TXT 업로드 → 질문 답변과 출처를 확인합니다.
9. 두 번째 이메일로 가입하고 승인 전 API 403, 승인 후 사용 가능, 서로 다른 문서 목록을 확인합니다.
10. Git 동기화 후 Vercel 재배포. 환경 변수 다섯 개(서버 3개, VITE_ 2개)를 설정합니다.

## 로컬 실행

프로젝트 루트 PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip install httpx python-multipart
.\.venv\Scripts\python.exe -m uvicorn main:app --app-dir backend --reload
```

새 터미널:

```powershell
cd frontend
npm install @supabase/supabase-js
npm run dev
```

`frontend/vite.config.js`의 `/api` 프록시는 로컬 FastAPI 서버(`http://127.0.0.1:8000`)를 향해야 합니다. 기존 Vercel 구성(`vercel.json`, `requirements.txt`)은 이전 배포에서 성공한 설정을 유지합니다.

## 보안 확인

- 로그아웃 상태: `/api/chat`은 401.
- 가입만 한 계정: `/api/chat`은 403.
- 승인된 계정: 본인 문서 읽기·추가·질문 가능.
- 다른 승인 계정: 첫 계정 문서가 보이지 않음.
- `GEMINI_API_KEY`와 Supabase secret/service-role 키가 Git·브라우저에 없음.

참고: https://supabase.com/docs/guides/api/using-custom-schemas · https://supabase.com/docs/guides/auth/general-configuration · https://supabase.com/docs/guides/database/postgres/row-level-security · https://supabase.com/docs/guides/getting-started/api-keys
