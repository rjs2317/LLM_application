from retrieval import load_chunks

# 작성한 함수를 실행하고 문단 수를 확인합니다.
chunks = load_chunks()
print("문단 수:", len(chunks))

# 처음 세 문단의 파일명과 앞 60글자만 봅니다.
for chunk in chunks[:3]:
    #print(chunk["source"], chunk["text"][:60])
    print("파일명 :", chunk["source"])
    print("내용 :", chunk["text"][:60])
    print()
    