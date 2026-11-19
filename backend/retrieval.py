"""SQLite의 문서를 문단으로 나누고 질문과 겹치는 단어를 찾습니다."""

from document_store import all_document_texts


def load_chunks():
    chunks = []
    for document in all_document_texts():
        # TXT 한 개의 내용을 빈 줄 기준으로 나눕니다.
        for paragraph in document["content"].split("\n\n"):
            paragraph = paragraph.strip()
            if paragraph:
                chunks.append(
                    {"source": document["filename"], "text": paragraph}
                )
    return chunks


def make_words(text):
    cleaned = text.lower()
    for mark in "?!,./:()-":
        cleaned = cleaned.replace(mark, " ")
    return cleaned.split()


def find_chunks(question):
    question_words = make_words(question)
    found = []

    for chunk in load_chunks():
        content_words = make_words(chunk["text"])
        for word in question_words:
            if len(word) > 1 and word in content_words:
                found.append(chunk)
                break
        if len(found) == 3:
            break
    return found
