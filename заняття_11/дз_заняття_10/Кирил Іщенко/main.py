import tkinter as tk
from PIL import Image, ImageTk
import requests
import re
import json



EMOTIONS = {
    "дякую": "happy",
    "клас": "happy",
    "помилка": "sad",
    "не працює": "sad",
    "вау": "surprised",
    "цікаво": "thinking",
}

COLORS = {"happy": "#FAC800", "sad": "#1100FF", "neutral": "#F30000",
          "thinking": "#12C438", "surprised": "#DF29F7"}
DEFAULT_PERSONA = {
    "id": "friend",
    "title": "Друг",
    "role": "дружній помічник-одноліток",
    "style": "тепло, на «ти», з легким гумором, коротко",
    "lexicon": ["класно", "давай разом", "без паніки"],
    "taboo": "не висміює помилок і не просить особистих даних",
    "greeting": "Привіт! Розкажеш, що в тебе нового?"
}

current = DEFAULT_PERSONA
PERSONAS = {}

def validate_persona(persona):
    errors = []
    required_fields = ["id", "title", "role", "style", "lexicon", "taboo", "greeting"]
    for field in required_fields:
        if field not in persona:
            errors.append(f"Відсутнє обов'язкове поле: {field}")
    if not persona.get("taboo"):
        errors.append("Поле taboo порожнє або відсутнє")
    if "lexicon" in persona:
        if not isinstance(persona["lexicon"], list):
            errors.append("Поле lexicon має бути списком")
    elif len(persona["lexicon"]) > 5:
        errors.append("Поле lexicon містить більше 5 слів")


def load_personas(path="urok10/personas.json"):
  with open(path, "r", encoding="utf-8") as file:
    items = json.load(file)

  valid_personas = {}
  for p in items:
    errors = validate_persona()
    if errors:
      print(f"Пропускаємо персону '{p.get('id', 'невідомо')}': {errors}")
    else:
      valid_personas[p["id"]] = p

  return valid_personas


TAG_RULE = (
    "Починай кожну відповідь тегом емоції в квадратних дужках: "
    "[happy], [sad], [neutral]"
)

def build_system_prompt(persona):
    return (
        f"Ти - S1tx, АІ-помічник у ролі: {persona['role']}. "
        f"Стиль: {persona['style']}. "
        f"Любиш вживати: {', '.join(persona['lexicon'])}. "
        f"Табу: {persona['taboo']}. "
        f"Відповідай у 1-3 реченнях. {TAG_RULE}"
    )
def find_persona(name):
    name = name.strip().lower()
    for persona in PERSONAS.values():
        if name in (persona["id"].lower(),
                    persona["title"].lower()):
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
    found = re.match(r"\s*\[(\w+)\]\s*", raw)
    if found and found.group(1).lower() in COLORS:
        return found.group(1).lower(), raw[found. end ():]
    return emotion_for(raw), raw

KEY = open("urok9/key.txt", encoding="utf-8").read().strip()
URL = "https://api.openai.com/v1/chat/completions"
HEAD = {"Authorization": "Bearer " + KEY}
def set_emotion(name):
    pic = Image.open("urok9/neutral.png").resize((300, 300))
    photo = ImageTk.PhotoImage(pic)
    face.config(image=photo)
    face.image = photo
    window.configure(bg=COLORS[name])

window = tk.Tk()
window.title("S1tx")
SYSTEM = ("Ти - S1tx дружній ШІ помічник Відповідай у 1-3 речення"
           "Починай кожнук відповідь тегом емоції в квадратних дужках: [happy], [sad],"
           "[suprised], [thinking] [neutral] а далі - текст відповіді")



pic = Image.open("urok9/neutral.png").resize((300, 300))
photo = ImageTk.PhotoImage(pic)
face = tk.Label(window, image=photo)
face.pack(pady=10)
face.image = photo

entry = tk.Entry(window, font=("Arial", 14), width=28)
entry.pack(pady=8)
answer = tk.Label(window, text="", font=("Arial", 14),
                  wraplength=360, justify="left")

def ask_ai(question):
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": question}
    ]
    data = {"model": "gpt-6-luna", "messages": messages}
    r = requests.post(URL, headers=HEAD, json=data)
    if r.status_code != 200:
        return "Помилка. Код: " + str(r.status_code)
    return r.json()["choices"][0]["message"]["content"]


def on_click():
    question = entry.get()
    entry.delete(0, tk.END)
    if not question:
        return
    set_emotion("neutral")
    answer.config(text="Думаю... : ")
    window.after(100, lambda: reply(question))

def reply(question):
    text = ask_ai(question)
    emotion, text = parse_reply(text)
    answer.config(text=text)
    set_emotion(emotion)





button = tk.Button(window, text="Запитати",
                   font=("Arial", 14), command=on_click)



button.pack(pady=4)
answer.pack(pady=10)

window.mainloop()

PERSONAS.update(load_personas())

switch_persona("Ворог")
print(current["title"])

switch_persona("Коуч")
print(current["title"])

switch_persona(" невідомо ")
print(current["title"])
validate_persona(PERSONAS)