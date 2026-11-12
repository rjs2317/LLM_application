from pathlib import Path
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()

def answer_question(question):
    document = Path("data/git_기초.txt").read_text(
        encoding="utf_8"
    )
    prompt = f"""아래 자료를 바탕으로 질문에 답하세요.
    자료에 없으면 찾을 수 없다고 말하세요.Path

    자료:
    {document}
 
    질문: {question}"""

    interaction = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=prompt,
)

    return interaction.output_text
