from retrieval import find_chunks

while True:
    question = input("질문 입력 (끝내려면 종료): ")
    if question == "종료":
        break  # 반복문을 끝냅니다.
    matches = find_chunks(question)
    print("찾은 문단 수:", len(matches))
    for match in matches:
        print("파일:", match["source"])
        print("내용 앞부분:", match["text"][:80])

