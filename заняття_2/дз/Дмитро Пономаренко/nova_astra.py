
import random

print("Привіт! Я Astra! 🚀")
print("Напиши 'стоп', щоб вийти.")

ANSWERS = {
    "музика": "Музика робить день кращим! 🎵"
}

JOKES = [
    "Чому комп'ютеру холодно? Бо Windows відкриті! 😂",
    "Що нуль сказав вісімці? Гарний ремінь! 😄",
    "Чому програмісти не люблять природу? Там багато багів!"
]


def analyze(text):
    text = text.lower().strip()

    if text in ["стоп", "вихід", "exit", "quit"]:
        return "вихід"

    if any(word in text for word in [
        "привіт", "привітик", "хай", "вітаю",
        "доброго ранку", "добрий день",
        "добрий вечір", "hello", "hi"
    ]):
        return random.choice([
            "Привіт! Рада тебе бачити! 😊",
            "О, привіт! Astra на зв'язку! 🚀",
            "Хай! Як твої справи?",
            "Вітаю! Що будемо робити?"
        ])

    if any(word in text for word in ["погод", "пгода", "pogoda"]):
        return "Я поки що не можу перевіряти погоду."

    if any(word in text for word in ["музик", "music"]):
        return ANSWERS["музика"]

    if any(word in text for word in [
        "жарт", "прикол", "розсміши", "joke"
    ]):
        return random.choice(JOKES)

    return "Я тебе почув! 🤖"


# Головний цикл Astra
while True:
    try:
        message = input("\nТи: ")
        answer = analyze(message)

        if answer == "вихід":
            print("Astra: До зустрічі! 👋")
            break

        print("Astra:", answer)

    except (KeyboardInterrupt, EOFError):
        print("\nAstra: До зустрічі! 👋")
        break
