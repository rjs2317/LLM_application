"""Supabase가 허용한 현재 사용자의 문서에서 문단을 검색합니다."""


def load_chunks(documents):
    chunks = []
    for document in documents:
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


def find_chunks(question, documents):
    question_words = make_words(question)
    found = []
    for chunk in load_chunks(documents):
        content_words = make_words(chunk["text"])
        for word in question_words:
            if len(word) > 1 and word in content_words:
                found.append(chunk)
                break
        if len(found) == 3:
            break
    return found
