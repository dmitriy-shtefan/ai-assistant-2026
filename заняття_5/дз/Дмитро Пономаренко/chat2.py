
import requests
import json
import os
import re

KEY = open("key.txt", encoding="utf-8").read().strip()
URL = "https://api.openai.com/v1/chat/completions"
HEAD = {"Authorization": "Bearer " + KEY}

MEMORY_FILE = "memory.json"
PERSONA_FILE = "persona.txt"

# Завантаження характеру ASTRA
DEFAULT_PERSONA = """
Ти ASTRA — розумний AI-помічник.
Відповідай українською мовою.
Допомагай із навчанням, математикою та програмуванням.
Спілкуйся дружньо, пояснюй зрозуміло.
Якщо знаєш ім'я користувача, звертайся до нього на ім'я.
"""

if not os.path.exists(PERSONA_FILE):
    with open(PERSONA_FILE, "w", encoding="utf-8") as f:
        f.write(DEFAULT_PERSONA.strip())

with open(PERSONA_FILE, "r", encoding="utf-8") as f:
    PERSONA = f.read().strip()

# Завантаження постійних фактів про користувача
try:
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        memory = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    memory = {}

# Системне повідомлення не входить до шести повідомлень
messages = [
    {"role": "system", "content": PERSONA}
]


def save_memory():
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=4)


def update_persona():
    facts = "\n".join(
        f"{key}: {value}"
        for key, value in memory.items()
    )

    messages[0]["content"] = PERSONA

    if facts:
        messages[0]["content"] += (
            "\n\nПостійна пам'ять про користувача:\n" + facts
        )


def remember(text):
    match = re.search(
        r"\bмене\s+звати\s+([А-ЯІЇЄҐA-Z][а-яіїєґa-z'-]*)",
        text,
        re.IGNORECASE
    )

    if match:
        name = match.group(1).capitalize()
        memory["ім'я користувача"] = name
        save_memory()
        update_persona()
        return name

    return None


def trim_history():
    # Залишаємо системний опис і останні 6 повідомлень
    while len(messages) > 7:
        messages.pop(1)


def ask(text):
    remember(text)

    messages.append({
        "role": "user",
        "content": text
    })

    trim_history()

    try:
        data = {
            "model": "gpt-6-luna",
            "messages": messages
        }

        r = requests.post(
            URL,
            headers=HEAD,
            json=data,
            timeout=30
        )

        if r.status_code != 200:
            messages.pop()
            return f"Помилка API: {r.status_code}\n{r.text}"

        answer = r.json()["choices"][0]["message"]["content"]

        messages.append({
            "role": "assistant",
            "content": answer
        })

        trim_history()
        return answer

    except requests.RequestException as e:
        if messages and messages[-1]["role"] == "user":
            messages.pop()

        return f"Помилка з'єднання: {e}"


def clear_chat():
    # Очищаємо розмову, але зберігаємо характер ASTRA
    messages.clear()
    messages.append({
        "role": "system",
        "content": PERSONA
    })
    update_persona()


def show_memory():
    count = len(messages) - 1

    print("\n" + "=" * 35)
    print("ПАМ'ЯТЬ ASTRA")
    print(f"Повідомлень у пам'яті: {count} / 6")
    print("=" * 35)

    if count == 0:
        print("Історія розмови порожня.")
    else:
        for message in messages[1:]:
            if message["role"] == "user":
                role = "Ти"
            else:
                role = "ASTRA"

            print(f"{role}: {message['content']}")

    print("=" * 35 + "\n")


update_persona()

print("=" * 35)
print("ASTRA — AI ASSISTANT")
print("=" * 35)
print("Я готова до розмови!")
print("Команди: очисти, пам'ять, стоп")
print("Пам'ять: останні 6 повідомлень.")
print()

while True:
    q = input("Ти: ").strip()
    command = q.lower()

    if command in ["стоп", "вихід", "exit"]:
        print("ASTRA: До зустрічі!")
        break

    if command == "очисти":
        clear_chat()
        print("ASTRA: Історію розмови очищено!")
        print("Мій характер збережено.")
        show_memory()
        continue

    if command == "пам'ять":
        show_memory()
        continue

    if not q:
        continue

    print("ASTRA:", ask(q))
    print(f"[Повідомлень у пам'яті: {len(messages) - 1} / 6]")
