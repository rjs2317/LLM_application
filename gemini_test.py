from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()

input_text = input("질문을 입력하세요 : ")

#print("질문",input_text,"답변",)

interaction = client.interactions.create(
    model="gemini-3.5-flash-lite",
    input="Git push을 한 문장으로 설명해 줘",
)
#print(interaction.output_text)
output_text = interaction.output_text

#print("질문",input_text,"답변",output_text)
#print(f"질문 : {input_text}, 답변 : {output_text}")

print(f"질문 : {input_text}")
print(f"답변 : {output_text}")