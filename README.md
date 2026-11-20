
# 오후 실습용 React 스타터

이 압축 파일의 `frontend` 폴더를 기존 `LLM_Application` 폴더에 넣으세요.

```text
LLM_Application/
├─ .env
├─ .gitignore
├─ data/git_기초.txt
├─ io_txt.py
└─ frontend/
```

VS Code 터미널에서 다음 명령을 실행합니다.

```powershell
cd frontend
npm install
npm run dev
```

브라우저에서 `http://localhost:5173`을 열면 임시 답변이 나오는 채팅 화면을 확인할 수 있습니다. 이후 수업에서 Python API를 만든 뒤 `src/App.jsx`의 `send()` 함수 안에 있는 임시 답변 부분을 API 호출로 바꿉니다.

API 키는 `frontend`에 넣지 마세요. 기존 프로젝트 루트의 `.env`를 Python 서버만 읽습니다.
