
import os
from gtts import gTTS
from playsound import playsound

# Створюємо папку для аудіо
os.makedirs("audio_cache", exist_ok=True)

def say(text, filename, lang="uk"):
    path = os.path.join("audio_cache", filename)

    if not os.path.exists(path):
        print("Створюю MP3:", path)
        audio = gTTS(text=text, lang=lang)
        audio.save(path)
        print("ЗБЕРЕЖЕНО!")

    else:
        print("Використовую готовий MP3:", path)

    playsound(path)


# 4 часті фрази
say("Привіт! Я ASTRA.", "hello.mp3")
say("Не розчула. Повтори.", "repeat.mp3")
say("Бувай!", "goodbye.mp3")
say("Гарного дня!", "goodday.mp3")

# Улюблена фраза трьома мовами
say("Булочка з сосискою!", "phrase_uk.mp3", "uk")
say("Sausage bun!", "phrase_en.mp3", "en")
say("Bułka z parówką!", "phrase_pl.mp3", "pl")
