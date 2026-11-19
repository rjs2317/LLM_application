from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).resolve().parent / "documents.db"
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

# 파일명 일부를 직접 입력해 봅니다. 빈칸이면 전체 목록입니다.
word = input("파일명에 포함된 단어: ").strip()
cursor.execute(
    "SELECT id, filename, content FROM documents WHERE filename LIKE ? ORDER BY id",
    ("%" + word + "%",),
)
rows = cursor.fetchall()

print("찾은 문서 수:", len(rows))
for row in rows:
    print("ID:", row[0], "파일:", row[1])
    print("내용 앞부분:", row[2][:80])

connection.close()
