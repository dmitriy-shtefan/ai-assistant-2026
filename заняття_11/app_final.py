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
    "або [neutral], а далі - текст відповіді."
)
PERSONAS = {}
history = []
MAX_HISTORY = 10
MAX_NOTES = 20
memory = {"name": "", "notes": []}


def load_memory(path="user.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        return {"name": "", "notes": []}
    name = data.get("name", "") if isinstance(data, dict) else ""
    notes = data.get("notes", []) if isinstance(data, dict) else []
    if not isinstance(name, str) or not isinstance(notes, list):
        return {"name": "", "notes": []}
    return {"name": name, "notes": [str(n) for n in notes][-MAX_NOTES:]}


def save_memory(path="user.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)


def memory_text():
    parts = []
    if memory["name"]:
        parts.append(f"Користувача звати {memory['name']}.")
    if memory["notes"]:
        parts.append("Користувач просив запам'ятати: " + "; ".join(memory["notes"]) + ".")
    return " ".join(parts)


def handle_command(text):
    low = text.lower().strip()
    if low.startswith("мене звати "):
        memory["name"] = text.strip()[len("мене звати "):].strip()[:30]
        save_memory()
        return f"Приємно познайомитись, {memory['name']}!"
    if low.startswith("запам'ятай ") or low.startswith("запамʼятай "):
        note = text.strip().split(maxsplit=1)[1][:100]
        memory["notes"] = (memory["notes"] + [note])[-MAX_NOTES:]
        save_memory()
        return "Записано: " + note
    if low in ("мої нотатки", "нотатки"):
        if not memory["notes"]:
            return "Нотаток поки немає."
        return "Нотатки: " + "; ".join(f"{i}) {n}" for i, n in enumerate(memory["notes"], 1))
    if low in ("забудь все", "забудь усе"):
        memory.update({"name": "", "notes": []})
        history.clear()
        save_memory()
        return "Готово, пам'ять очищено."
    if low in ("допомога", "help"):
        return "Команди: мене звати ...; запам'ятай ...; мої нотатки; забудь все."
    return None


def add_message(role, text):
    history.append({"role": role, "content": text})
    del history[:-MAX_HISTORY]
    while history and history[0]["role"] != "user":
        history.pop(0)


def load_personas(path="personas.json"):
    with open(path, "r", encoding="utf-8") as file:
        items = json.load(file)

    return {p["id"]: p for p in items}


def build_system_prompt(persona):
    base = (
        f"Ти - АІДА, AI-помічник у ролі: {persona['role']}. "
        f"Стиль: {persona['style']}. Любиш вживати: {', '.join(persona['lexicon'])}. "
        f"Табу: {persona['taboo']}. Відповідай у 1-3 реченнях. {TAG_RULE}"
    )

    mem = memory_text()
    return base + (" " + mem if mem else "")


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
        {"role": "system", "content": build_system_prompt(current)}
    ] + history + [{"role": "user", "content": question}]
    data = {"model": "gpt-6-luna", "messages": messages}
    r = requests.post(URL, headers=HEAD, json=data)
    if r.status_code != 200:
        return "Помилка. Код: " + str(r.status_code)
    text = r.json()["choices"][0]["message"]["content"]
    if not isinstance(text, str):
        return "Помилка: API повернув відповідь без тексту."

    add_message("user", question)
    add_message("assistant", text)
    return text


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
    text = handle_command(question)
    if text is not None:
        set_emotion("happy")
        answer.config(text=text)
        return

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
current = PERSONAS.get("friend", DEFAULT_PERSONA)
memory.update(load_memory())

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
