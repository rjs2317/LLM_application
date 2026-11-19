from pathlib import Path
import sqlite3

# 실행 위치가 달라도 이 파일의 폴더를 기준으로 찾습니다.
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "documents.db"
DATA_DIR = BASE_DIR / "data"

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

# 문서 한 개를 한 행으로 저장할 표를 만듭니다.
cursor.execute("""
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL UNIQUE,
    content TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

# 제공된 TXT 파일을 읽어 DB에 넣습니다.
for path in sorted(DATA_DIR.glob("*.txt")):
    cursor.execute("SELECT id FROM documents WHERE filename = ?", (path.name,))
    if cursor.fetchone() is None:
        text = path.read_text(encoding="utf-8")
        cursor.execute(
            "INSERT INTO documents (filename, content) VALUES (?, ?)",
            (path.name, text),
        )
        print("추가:", path.name)
    else:
        print("이미 있음:", path.name)

connection.commit()  # 변경 내용을 DB 파일에 저장합니다.
cursor.execute("SELECT COUNT(*) FROM documents")
print("문서 수:", cursor.fetchone()[0])
connection.close()
