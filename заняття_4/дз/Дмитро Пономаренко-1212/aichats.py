import requests

# Завантаження API-ключа
with open("key.txt", encoding="utf-8") as f:
    KEY = f.read().strip()

URL = "https://api.openai.com/v1/chat/completions"

headers = {
    "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json"
}


# Функція штучного інтелекту ASTRA
def ask_ai(question):
    data = {
        "model": "gpt-6-luna",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Твоє ім'я — ASTRA. "
                    "Ти дружній штучний інтелект. "
                    "Відповідай українською мовою, "
                    "зрозуміло та цікаво."
                )
            },
            {
                "role": "user",
                "content": question
            }
        ]
    }

    try:
        r = requests.post(
            URL,
            headers=headers,
            json=data,
            timeout=30
        )

        if r.status_code != 200:
            try:
                error = r.json().get("error", {}).get(
                    "message", "Невідома помилка"
                )
            except ValueError:
                error = "Не вдалося прочитати відповідь сервера."

            return f"Помилка API ({r.status_code}): {error}"

        result = r.json()
        return result["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as error:
        return f"Помилка з'єднання: {error}"

    except (KeyError, IndexError, ValueError):
        return "ASTRA не змогла прочитати відповідь сервера."


# Тестування ASTRA
tests = [
    "Привіт! Хто ти?",
    "Поясни простими словами, що таке Python.",
    "Придумай коротку мотиваційну фразу."
]

print("=" * 40)
print("ТЕСТУВАННЯ ASTRA")
print("=" * 40)

for i, question in enumerate(tests, start=1):
    print(f"\nТест {i}: {question}")
    answer = ask_ai(question)
    print("ASTRA:", answer)


# Основний цикл спілкування
print("\n" + "=" * 40)
print("ASTRA готова до спілкування!")
print("Напиши 'стоп', щоб завершити.")
print("=" * 40)

while True:
    question = input("\nТи: ").strip()

    if question.lower() in ["стоп", "вихід", "exit"]:
        print("ASTRA: До зустрічі! Гарного дня!")
        break

    if not question:
        print("ASTRA: Напиши запитання, і я відповім!")
        continue

    print("\nASTRA думає...")
    print("ASTRA:", ask_ai(question))