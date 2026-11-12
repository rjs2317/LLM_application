from chat_service import answer_question

# sum = 0
# for num in range(1,11):
#     sum += num
#     print(sum)
#     if sum == 21:
#         break

#     print(sum)
#     print(f"1부터10까지의 총 합: {sum}")

#     total = 0
#     number = 1
#     while(number <= 10):  # 참(True)일때에만 whlie 반복문이 실행
#         total += number
#         number = number + 1
#         print(total)
# print (f"1부터10까지의 총 합 : {total}")

while True:

    question = input("질문(종료:q): "). strip()
    if question == "q":
        print("대화를 종료합니다.")
        break
    if not question:
        print("질문을 입력 해주세요 : ")
        continue

    answer = answer_question(question)
    print("답변:", answer)
    print()



