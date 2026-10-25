
import os
import requests

def ask_ai(question):
    key = os.getenv("OPENAI_API_KEY")

    if not key:
        return "Немає API-ключа"

    r = requests.post(
        "https://api.openai.com/v1/responses",
        headers={"Authorization": "Bearer " + key},
        json={"model": "gpt-4.1-mini", "input": question}
    )

    return r.json()["output"][0]["content"][0]["text"]


questions = [
    "Що таке Python?",
    "Скільки буде 2+2?",
    "Що таке ШІ?"
]

for q in questions:
    print("Питання:", q)
    print("Відповідь:", ask_ai(q))
    print()
