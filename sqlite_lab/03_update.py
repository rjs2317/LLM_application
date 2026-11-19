from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).resolve().parent / "documents.db"
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

# 02_read.py에서 확인한 문서 ID를 입력합니다.
document_id = int(input("수정할 문서 ID: "))
new_name = input("새 파일명: ").strip()

if new_name:
    cursor.execute(
        "UPDATE documents SET filename = ? WHERE id = ?",
        (new_name, document_id),
    )
    connection.commit()
    print("수정된 행 수:", cursor.rowcount)
else:
    print("새 파일명이 비어 있어 수정하지 않았습니다.")

connection.close()
