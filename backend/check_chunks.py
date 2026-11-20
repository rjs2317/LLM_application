from retrieval import load_chunks

chunks = load_chunks()
print("문단 수:", len(chunks))

for chunk in chunks[:3]:
    print(chunk["source"], chunk["text"][:60])

# 실행 명령은 Python 파일이 아닌 터미널에 입력:
# .\.venv\Scripts\python.exe backend/check_chunks.py
