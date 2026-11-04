import os
import uuid
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import requests

KEY = open("key.txt", encoding="utf-8").read().strip()

URL = "https://api.openai.com/v1/chat/completions"

HEADER = {
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json"
}

PERSONA = """
Ти ASTRA — розумний голосовий AI-помічник.

Твоє ім'я ASTRA.
Ти ніколи не називаєш себе ChatGPT.
Якщо тебе запитують, як тебе звати,
відповідай: Мене звати ASTRA!

Спілкуйся виключно українською мовою.
Будь ввічливою, розумною та дружньою.
Допомагай із навчанням, програмуванням
та відповідай на різні запитання.
"""

def ask_ai(question):
    data = {
        "model": "gpt-6-luna",
        "messages": [
            {"role": "system", "content": PERSONA},
            {"role": "user", "content": question}
        ]
    }

    try:
        response = requests.post(
            URL,
            headers=HEADER,
            json=data,
            timeout=30
        )

        if response.status_code != 200:
            return "Помилка. Код: " + str(response.status_code)

        return response.json()["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException:
        return "Не вдалося підключитися до сервера."


r = sr.Recognizer()


def say(text):
    os.makedirs("audio_cache", exist_ok=True)

    name = os.path.join(
        "audio_cache",
        f"answer_{uuid.uuid4().hex}.mp3"
    )

    try:
        gTTS(text, lang="uk").save(name)
        playsound(name)

    except Exception as error:
        print("Помилка озвучення:", error)

    finally:
        if os.path.exists(name):
            try:
                os.remove(name)
            except OSError:
                pass


def listen():
    with sr.Microphone() as mic:
        r.adjust_for_ambient_noise(mic, duration=1)

        print("Говори...")

        audio = r.listen(mic, phrase_time_limit=8)

    try:
        return r.recognize_google(
            audio,
            language="uk-UA"
        )

    except sr.UnknownValueError:
        return ""

    except sr.RequestError:
        print("Помилка розпізнавання голосу.")
        return ""


print("=" * 35)
print("       ASTRA AI ASSISTANT")
print("=" * 35)

os.makedirs("audio_cache", exist_ok=True)

while True:
    text = listen()

    if text == "":
        continue

    print("Ти:", text)

    if "стоп" in text.lower():
        print("ASTRA: Бувай!")
        say("Бувай! До наступної зустрічі!")
        break

    answer = ask_ai(text)

    print("ASTRA:", answer)

    say(answer)