import random
from datetime import datetime

def analyze(text):
    text = text.lower()

    if "жарт" in text:
        return "жарт"

    if "час" in text or "годин"in text:
        return "час"

    if "музик"in text:
        return "музика"

    if "погод" in text:
        return "погода"
    return "невідомо"


def answer(tema):
    if tema == "час":
        return datetime.now().strftime("Зараз %H:%M")
    if tema == "жарт":
        return random.choice(JOKES)
    return ANSWERS[tema]


ANSWERS = {
    "жарт": "Чому робот пішов спати? Розрядився.",
    "час": "Годинник ще не підключив, вибач.",
    "погода": "Вікна не бачу, але вір у сонце!",
    "музика": 'Моя улюбленна музика це електронна',
    "невідомо": "Я ще вчуся. Спитай про жарт, час чи погоду.",
}

JOKES = ["Робот пішов спати - розрядився.",
         "Мій улюбленний формат - .txt, він не сперечаеться"
         "На світі є 10 типів людей: ті, хто розуміють двійкову систему числення, і ті, хто її не розуміє."]

MOOD = random.choice(["бадьорий", "сонний", "жартівливий"])
PREFIX = {
    "бадьорий": "Ого! ",
    "сонний": "Мм... ",
    "жартівливий": "Ха! ",
}

while True:
    text = input("Ти: ")
    if text.lower() == "стоп":
        print("S1tx: Бувай!")
        break
    print("S1tx: " + PREFIX[MOOD] + answer(analyze(text)))