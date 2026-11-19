from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).resolve().parent / "documents.db"
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

# 삭제할 행을 먼저 보여 줍니다.
document_id = int(input("삭제할 문서 ID: "))
cursor.execute("SELECT filename FROM documents WHERE id = ?", (document_id,))
row = cursor.fetchone()

if row is None:
    print("해당 ID의 문서가 없습니다.")
else:
    print("삭제 대상:", row[0])
    confirm = input("정말 지우려면 '삭제' 입력: ")
    if confirm == "삭제":
        cursor.execute("DELETE FROM documents WHERE id = ?", (document_id,))
        connection.commit()
        print("삭제된 행 수:", cursor.rowcount)
    else:
        print("삭제를 취소했습니다.")

connection.close()
