# SQLite로 문서 자료를 데이터베이스화하기

소요 시간: 50분 실습 + 10분 휴식. VS Code에서 기존 `LLM_Application` 폴더를 열고, 이 폴더를 프로젝트 루트에 `sqlite_lab`이라는 이름으로 넣습니다. Python의 `sqlite3`는 기본 제공 모듈이므로 별도 설치가 필요하지 않습니다.

## 실행 순서

프로젝트 루트 터미널에서 차례대로 실행합니다.

```powershell
.\.venv\Scripts\python.exe sqlite_lab\01_import.py
.\.venv\Scripts\python.exe sqlite_lab\02_read.py
.\.venv\Scripts\python.exe sqlite_lab\03_update.py
.\.venv\Scripts\python.exe sqlite_lab\04_delete.py
```

가상환경이 없으면 `python`으로 실행할 수 있습니다. `sqlite_lab/documents.db`는 첫 번째 명령을 실행할 때 생성됩니다. 이 파일은 개인 실습 결과이며, 자료에 따라 민감한 내용이 들어갈 수 있으므로 GitHub에 올리지 않습니다. 프로젝트의 `.gitignore`에 `sqlite_lab/*.db`를 추가합니다.

## 관찰할 것

1. `01_import.py`: 세 TXT 파일이 `documents` 테이블의 세 행으로 들어가는지 확인합니다. 다시 실행해도 중복 행이 생기지 않는지 살펴봅니다.
2. `02_read.py`: `linux`, `git`, `cicd`처럼 파일명 일부를 입력하고 조회합니다. 아무 글자도 입력하지 않으면 전체 목록을 봅니다.
3. `03_update.py`: 출력된 문서 ID 하나를 고르고 다른 파일명으로 바꿉니다. **DB의 파일명만** 바뀌며 원본 TXT 파일 이름은 그대로인지 비교합니다.
4. `04_delete.py`: ID로 한 행을 삭제합니다. 확인 단어 `삭제`를 입력하기 전에는 지워지지 않는지 확인합니다. 원본 TXT 파일은 삭제되지 않습니다.

## 보안과 연결할 질문

- `WHERE id = ?`가 없다면 `UPDATE`와 `DELETE`는 몇 행에 적용될까요?
- 사용자 입력을 SQL 문자열에 직접 붙이는 대신 `?`와 값의 묶음을 전달하는 이유는 무엇일까요?
- `documents.db` 파일을 다른 사람이 복사하면 그 안의 텍스트를 읽을 수 있을까요?

SQLite는 내 PC의 DB 파일을 직접 사용합니다. 다음 Supabase 실습에서는 같은 테이블·행·SQL 개념을 네트워크의 PostgreSQL에 적용하고, 누가 접근할 수 있는지도 설정합니다.

참고: https://docs.python.org/3/library/sqlite3.html
