from pathlib import Path

# retrieval.py가 있는 폴더(backend) 안의 data 폴더
DATA_DIR = Path(__file__).resolve().parent / "data"

# 사용자 정의 함수 만들기
def load_chunks():
    chunks = []  # 문단을 담을 빈 목록
    # data 폴더의 TXT 파일을 하나씩 읽습니다.
    for path in sorted(DATA_DIR.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        # 빈 줄을 기준으로 문단을 나눕니다.
        for paragraph in text.split("\n\n"):
            paragraph = paragraph.strip()
            if paragraph:  # 비어 있지 않은 문단만 저장
                chunks.append({
                    "source": path.name,  # 원본 파일명
                    "text": paragraph,    # 문단 내용
                })
    return chunks

def make_words(text):
    cleaned = text.lower()
    for mark in "?!,./:()-":
        cleaned = cleaned.replace(mark,"")
    return cleaned.split()

def find_chunks(question):
    # 질문을 단어 목록으로 바꿉니다.
    question_words = make_words(question)
    found = []
    for chunk in load_chunks():
        content_words = make_words(chunk["text"])
        for word in question_words:
            # 같은 단어가 있으면 이 문단을 저장합니다.
            if len(word) > 1 and word in content_words:
                found.append(chunk)
                break  # 같은 문단은 한 번만 저장
        if len(found) == 3:
            break  # 세 문단을 찾았으면 검색 종료
    return found
