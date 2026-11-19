"""SQLite에 저장된 수업 문서를 읽고 추가합니다."""

import sqlite3
from pathlib import Path


# 이 파일은 backend 안에 있고, DB는 앞 실습의 sqlite_lab 안에 있습니다.
PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_DIR / "sqlite_lab" / "documents.db"


def open_db():
    DB_PATH.parent.mkdir(exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.execute(
        "CREATE TABLE IF NOT EXISTS documents ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "filename TEXT NOT NULL UNIQUE, "
        "content TEXT NOT NULL, "
        "created_at TEXT DEFAULT CURRENT_TIMESTAMP)"
    )
    connection.commit()
    return connection


def list_documents():
    connection = open_db()
    rows = connection.execute(
        "SELECT id, filename, created_at FROM documents ORDER BY id"
    ).fetchall()
    connection.close()

    documents = []
    for row in rows:
        documents.append(
            {"id": row[0], "filename": row[1], "created_at": row[2]}
        )
    return documents


def all_document_texts():
    connection = open_db()
    rows = connection.execute(
        "SELECT filename, content FROM documents ORDER BY id"
    ).fetchall()
    connection.close()

    documents = []
    for row in rows:
        documents.append({"filename": row[0], "content": row[1]})
    return documents


def add_document(filename, content):
    connection = open_db()
    existing = connection.execute(
        "SELECT id FROM documents WHERE filename = ?", (filename,)
    ).fetchone()
    if existing:
        connection.close()
        return None

    cursor = connection.execute(
        "INSERT INTO documents (filename, content) VALUES (?, ?)",
        (filename, content),
    )
    connection.commit()
    document_id = cursor.lastrowid
    connection.close()
    return document_id
