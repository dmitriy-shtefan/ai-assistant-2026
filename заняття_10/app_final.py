import tkinter as tk
import re

from PIL import Image, ImageTk
import requests
import json

SYSTEM = (
    "Ти - АІДА, дружній АІ-помічник. Відповідай у 1-3 речення. "
    "Починай кожну відповідь тегом емоції в квадратних дужках: [happy], [sad], "
    "[surprised], [thinking] або [neutral], а далі - текст відповіді."
)

KEY = open("key.txt", encoding="utf-8").read().strip()
URL = "https://api.openai.com/v1/chat/completions"
HEAD = {"Authorization": "Bearer " + KEY}


COLORS = {"happy": "#FFF3C4", "sad": "#D6E4F0",
          "neutral": "#F1EFE8"}
EMOTIONS = {"дякую": "happy", "клас": "happy",
            "помилка": "sad", "не працює": "sad"}

DEFAULT_PERSONA = {
    "id": "friend", "title": "Друг", "role": "дружній помічник", "style": "тепло й коротко",
    "lexicon": [], "taboo": "не просить особистих даних", "greeting": "Привіт!",
}
current = DEFAULT_PERSONA
TAG_RULE = (
    "Починай кожну відповідь тегом емоції в квадратних дужках: [happy], [sad] "
    "або [neutral], а далі — текст відповіді."
)
PERSONAS = {}

def load_personas(path="personas.json"):
    with open(path, "r", encoding="utf-8") as file:
        items = json.load(file)

    return {p["id"]: p for p in items}



def build_system_prompt(persona):
    return (
        f"Ти — АІДА, AI-помічник у ролі: {persona['role']}. "
        f"Стиль: {persona['style']}. Любиш вживати: {', '.join(persona['lexicon'])}. "
        f"Табу: {persona['taboo']}. Відповідай у 1–3 реченнях. {TAG_RULE}"
    )


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


def emotion_for(text):
    text = text.lower()
    for word, emotion in EMOTIONS.items():
        if word in text:
            return emotion
    return "neutral"


def parse_reply(raw):
    """Відокремлює тег емоції [happy] від тексту. Немає тегу - визначаємо за словом"""
    found = re.match(r"\s*\[(\w+)\]\s*", raw)
    if found and found.group(1).lower() in COLORS:
        return found.group(1).lower(), raw[found. end () :]
    return emotion_for(raw), raw


def ask_ai(question):
    messages = [
        {"role": "system", "content": build_system_prompt(current)},
        {"role": "user", "content": question}
    ]
    data = {"model": "gpt-6-luna", "messages": messages}
    r = requests.post(URL, headers=HEAD, json=data)
    if r.status_code != 200:
        return "Помилка. Код: " + str(r.status_code)
    return r.json()["choices"][0]["message"]["content"]


def set_emotion(name):
    pic = Image.open(name + ".png").resize((300, 300))
    photo = ImageTk.PhotoImage(pic)
    face.config(image=photo)
    face.image = photo
    window.configure(bg=COLORS[name])


def on_click():
    question = entry.get()
    entry.delete(0, tk.END)
    if not question:
        return
    set_emotion("neutral")
    answer.config(text="Думаю...")
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
        

window = tk.Tk()
window.title("АІДА")

PERSONAS.update(load_personas())

titles = [p["title"] for p in PERSONAS.values()]
persona_var = tk.StringVar(value=current["title"])
menu = tk.OptionMenu(window, persona_var, *titles, command=on_persona)
menu.pack(pady=4)

pic = Image.open("neutral.png").resize((300, 300))
photo = ImageTk.PhotoImage(pic)
face = tk.Label(window, image=photo)
face.pack(pady=10)
face.image = photo

entry = tk.Entry(window, font=("Arial", 14), width=28)
entry.pack(pady=8)

answer = tk.Label(window, text="", font=("Arial", 13),
                  wraplength=360, justify="left")

button = tk.Button(window, text="Запитати",
                   font=("Arial", 14), command=on_click)
button.pack(pady=4)

answer.pack(pady=10)

window.mainloop()
