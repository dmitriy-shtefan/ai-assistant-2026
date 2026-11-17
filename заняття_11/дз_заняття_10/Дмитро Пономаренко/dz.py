import json
import os
import re
import tkinter as tk

import requests
from PIL import Image, ImageTk

from emotions import emotion_for


COLORS = {
    "happy": "#FFF3C4",
    "sad": "#D6E4F0",
    "neutral": "#F1EFE8",
}

EMOTIONS = {
    "дякую": "happy",
    "клас": "happy",
    "помилка": "sad",
    "не працює": "sad",
}

DEFAULT_PERSONA = {
    "id": "friend",
    "title": "Друг",
    "role": "дружній помічник-одноліток",
    "style": "тепло, на «ти», з легким гумором, коротко",
    "lexicon": ["класно", "давай разом", "без паніки", "ти красавчик!"],
    "taboo": "не висміює помилок і не просить особистих даних",
    "greeting": "Привіт! Розкажеш, що в тебе нового?",
}

current = DEFAULT_PERSONA
PERSONAS = {}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def validate_persona(persona):
    problems = []
    required_fields = [
        "id",
        "title",
        "role",
        "style",
        "lexicon",
        "taboo",
        "greeting",
    ]

    # Перевіряємо відсутні поля
    for field in required_fields:
        if field not in persona:
            problems.append("Відсутнє поле: " + field)

    # Перевіряємо taboo
    if "taboo" in persona and not str(persona["taboo"]).strip():
        problems.append("Поле taboo порожнє")

    # Перевіряємо lexicon
    if "lexicon" in persona:
        if not isinstance(persona["lexicon"], list):
            problems.append("Lexicon повинен бути списком")
        elif len(persona["lexicon"]) > 5:
            problems.append("У lexicon більше 5 слів")

    return problems


def load_personas(path="personas.json"):
    full_path = os.path.join(BASE_DIR, path)
    with open(full_path, "r", encoding="utf-8") as file:
        items = json.load(file)

    valid_personas = {}
    for persona in items:
        problems = validate_persona(persona)
        if problems:
            print("Персона пропущена:", persona.get("id", "невідома"))
            for problem in problems:
                print(" -", problem)
        else:
            valid_personas[persona["id"]] = persona

    return valid_personas


PERSONAS.update(load_personas())
print(list(PERSONAS))

TAG_RULE = (
    "Починай кожну відповідь тегом емоції в квадратних дужках:"
    " [happy], [sad] або [neutral], а далі - текст відповіді."
)


def build_system_prompt(persona):
    return (
        f"Ти - ASTRA, AI-помічник у ролі: {persona['role']}. "
        f"Стиль: {persona['style']}. "
        f"Любиш вживати: {', '.join(persona['lexicon'])}. "
        f"Табу: {persona['taboo']}. "
        f"Відповідай у 1-3 реченнях. {TAG_RULE} "
    )


print(build_system_prompt(PERSONAS["mentor"]))
print(build_system_prompt(PERSONAS["coach"]))


def find_persona(name):
    name = name.strip().lower()
    for persona in PERSONAS.values():
        if name in (persona["id"].lower(), persona["title"].lower()):
            return persona
    return None


def switch_persona(name):
    global current
    persona = find_persona(name)
    if persona is not None:
        current = persona
    return persona


print(PERSONAS)
switch_persona(" вЧИТЕЛЬ ")
print(current["title"])
switch_persona("coach")
print(current["title"])
switch_persona("невідомо")
print(current["title"])


def emotion_for(text):
    text = text.lower()
    for word, emotion in EMOTIONS.items():
        if word in text:
            return emotion
    return "neutral"


def parse_reply(raw):
    found = re.match(r"\s*\[(\w+)\]\s*", raw)
    if found and found.group(1).lower() in COLORS:
        return found.group(1).lower(), raw[found.end():]
    return emotion_for(raw), raw


SYSTEM = (
    "Ти - ASTRA, дружній AI-помічник. Відповідай у 1-3 речення."
    "Починай кожну відповідь тегом емоції в квадратних дужках: [happy], [sad],"
    " [surprized] або [neutral], а далі - текст відповіді."
)

KEY = open(os.path.join(BASE_DIR, "key.txt"), encoding="utf-8").read().strip()
URL = "https://api.openai.com/v1/chat/completions"
HEAD = {"Authorization": "Bearer " + KEY}


def set_emotion(name):
    pic = Image.open(os.path.join(BASE_DIR, name + ".jpg")).resize((300, 300))
    photo = ImageTk.PhotoImage(pic)
    face.config(image=photo)
    face.image = photo
    window.configure(bg=COLORS[name])


def ask_ai(question):
    messages = [
        {"role": "system", "content": build_system_prompt(current)},
        {"role": "user", "content": question},
    ]
    data = {"model": "gpt-6-luna", "messages": messages}
    r = requests.post(URL, headers=HEAD, json=data)
    if r.status_code != 200:
        return "Помилка, Код: " + str(r.status_code)
    return r.json()["choices"][0]["message"]["content"]


def on_click():
    question = entry.get()
    entry.delete(0, tk.END)
    if not question:
        return
    set_emotion("neutral")
    answer.config(text="Я думаю...")
    window.after(100, lambda: reply(question))


def reply(question):
    text = ask_ai(question)
    emotion, text = parse_reply(text)
    answer.config(text=text)
    set_emotion(emotion)


def on_persona(title):
    persona = switch_persona(title)
    if persona is not None:
        persona_var.set(persona["title"])
        set_emotion("happy")
        answer.config(text=persona["greeting"])
        taboo_label.config(text="Табу: " + persona["taboo"])


window = tk.Tk()
window.title("ASTRA")

pic = Image.open(os.path.join(BASE_DIR, "neutral.jpg")).resize((300, 300))
photo = ImageTk.PhotoImage(pic)
face = tk.Label(window, image=photo)
face.pack(pady=20)
face.image = photo

entry = tk.Entry(window, font=("Arial", 14), width=28)
entry.pack(pady=8)

answer = tk.Label(
    window,
    text="",
    font=("Arial", 13),
    wraplength=350,
    justify="left",
)
answer.pack(pady=8)

PERSONAS.update(load_personas())
title = [persona["title"] for persona in PERSONAS.values()]
persona_var = tk.StringVar(value=current["title"])
menu = tk.OptionMenu(window, persona_var, *title, command=on_persona)
menu.pack(pady=4)

button = tk.Button(window, text="Запитати", font=("Arial", 14), command=on_click)
button.pack(pady=4)
button.pack(pady=8)

taboo_label = tk.Label(
    window,
    text="Табу: " + current["taboo"],
    font=("Arial", 10),
    wraplength=350,
    justify="left",
)
taboo_label.pack(pady=10)

window.mainloop()