import requests
import json
import re
import tkinter as tk
from PIL import Image, ImageTk

COLORS = {
    "happy": "#FFF3C4",
    "sad": "#D6E4F0",
    "neutral": "#F1EFE8"
}

EMOTIONS = {
    "дякую": "happy",
    "клас": "happy",
    "помилка": "sad",
    "не працює": "sad"
}

DEFAULT_PERSONA = {
    "id": "friend",
    "title": "Друг",
    "role": "дружній помічник-одноліток",
    "style": "тепло, на «ти», з легким гумором, коротко",
    "lexicon": ["класно", "давай разом", "без паніки", "ти красавчик!"],
    "taboo": "не висміює помилок і не просить особистих даних",
    "greeting": "Привіт! Розкажеш, що в тебе нового?"
}

REQUIRED_FIELDS = (
    "id", "title", "role", "style", "lexicon", "taboo", "greeting"
)


def validate_persona(persona):
    problems = []

    if not isinstance(persona, dict):
        return ["дані персони мають бути словником"]

    for field in REQUIRED_FIELDS:
        if field not in persona:
            problems.append(f"відсутнє поле «{field}»")

    if "taboo" in persona:
        if not isinstance(persona["taboo"], str) or not persona["taboo"].strip():
            problems.append("поле «taboo» порожнє")

    if "lexicon" in persona:
        if not isinstance(persona["lexicon"], list):
            problems.append("поле «lexicon» має бути списком")
        elif len(persona["lexicon"]) > 5:
            problems.append("лексикон містить більше 5 слів")

    return problems


def load_personas(path="personas.json"):
    try:
        with open(path, "r", encoding="utf-8") as file:
            items = json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        print(f"Не вдалося завантажити файл: {error}")
        return {}

    if not isinstance(items, list):
        print("Помилка: очікується список персон.")
        return {}

    valid_personas = {}

    for number, persona in enumerate(items, start=1):
        problems = validate_persona(persona)

        if problems:
            name = (
                persona.get("title", f"персона №{number}")
                if isinstance(persona, dict)
                else f"персона №{number}"
            )
            print(f"Персону «{name}» пропущено: {'; '.join(problems)}.")
            continue

        valid_personas[persona["id"]] = persona

    return valid_personas


PERSONAS = {"friend": DEFAULT_PERSONA}
PERSONAS.update(load_personas())

print("Завантажені персони:", list(PERSONAS))


TAG_RULE = (
    "Починай кожну відповідь тегом емоції в квадратних дужках:"
    " [happy], [sad] або [neutral], а далі — текст відповіді."
)


def build_system_prompt(persona):
    return (
        f"Ти — ASTRA, AI-помічник у ролі: {persona['role']}. "
        f"Стиль: {persona['style']}. "
        f"Любиш вживати: {', '.join(persona['lexicon'])}. "
        f"Табу: {persona['taboo']}. "
        f"Відповідай у 1–3 реченнях. {TAG_RULE}"
    )


current = DEFAULT_PERSONA


def find_persona(name):
    name = name.strip().lower()

    for persona in PERSONAS.values():
        if name in (
            persona["id"].lower(),
            persona["title"].lower()
        ):
            return persona

    return None


def switch_persona(name):
    global current

    persona = find_persona(name)

    if persona is not None:
        current = persona
        taboo_label.config(text=f"Табу: {current['taboo']}")
        persona_var.set(current["title"])

    return persona


def emotion_for(text):
    text = text.lower()

    for word, emotion in EMOTIONS.items():
        if word in text:
            return emotion

    return "neutral"


def parse_reply(raw):
    found = re.match(r"\[(\w+)\]\s*(.*)", raw)

    if found and found.group(1) in COLORS:
        return found.group(1), found.group(2)

    return emotion_for(raw), raw


try:
    with open("key.txt", encoding="utf-8") as file:
        KEY = file.read().strip()
except OSError:
    KEY = ""
    print("Не знайдено файл key.txt з API-ключем.")


URL = "https://api.openai.com/v1/chat/completions"
HEAD = {"Authorization": "Bearer " + KEY}


def set_emotion(name):
    if name not in COLORS:
        name = "neutral"

    pic = Image.open(name + ".jpg").resize((300, 300))
    photo = ImageTk.PhotoImage(pic)

    face.config(image=photo)
    face.image = photo

    window.configure(bg=COLORS[name])


window = tk.Tk()
window.title("ASTRA")

pic = Image.open("neutral.jpg").resize((300, 300))
photo = ImageTk.PhotoImage(pic)

face = tk.Label(window, image=photo)
face.pack(pady=20)
face.image = photo


persona_var = tk.StringVar(value=current["title"])

persona_menu = tk.OptionMenu(
    window,
    persona_var,
    *[persona["title"] for persona in PERSONAS.values()],
    command=switch_persona
)

persona_menu.config(font=("Arial", 12))
persona_menu.pack(pady=4)


entry = tk.Entry(window, font=("Arial", 14), width=28)
entry.pack(pady=8)


answer = tk.Label(
    window,
    text="",
    font=("Arial", 13),
    wraplength=350,
    justify="left"
)

answer.pack(pady=8)


def ask_ai(question):
    messages = [
        {"role": "system", "content": build_system_prompt(current)},
        {"role": "user", "content": question}
    ]

    data = {
        "model": "gpt-6-luna",
        "messages": messages
    }

    try:
        response = requests.post(
            URL,
            headers=HEAD,
            json=data,
            timeout=30
        )
    except requests.RequestException as error:
        return f"[sad] Не вдалося під'єднатися до сервера: {error}"

    if response.status_code != 200:
        return "[sad] Помилка, код: " + str(response.status_code)

    try:
        return response.json()["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError, ValueError):
        return "[sad] Не вдалося прочитати відповідь сервера."


def on_click():
    question = entry.get().strip()
    entry.delete(0, tk.END)

    if not question:
        return

    set_emotion("neutral")
    answer.config(text="Я думаю...")

    window.after(100, lambda: reply(question))


def reply(question):
    response_text = ask_ai(question)

    emotion, response_text = parse_reply(response_text)

    answer.config(text=response_text)
    set_emotion(emotion)


button = tk.Button(
    window,
    text="Запитати",
    font=("Arial", 14),
    command=on_click
)

button.pack(pady=8)


# Мітка табу в нижній частині вікна
taboo_label = tk.Label(
    window,
    text=f"Табу: {current['taboo']}",
    font=("Arial", 10),
    wraplength=380,
    justify="left"
)

taboo_label.pack(side="bottom", pady=10)


window.mainloop()