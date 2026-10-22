import random
from datetime import datetime
def analyze(text):
    text = text.lower()
    if "жарт" in text:
        return"жарт"
    elif "привіт" in text:
        return "привіт"
    elif "погода" in text:
        return "погода"
    elif "музик" in text:
            return "музик"
    elif "час" in text:
            return "час"
    return "невідомо"

ANSWERS = {
    "жарт": "Чому робот пішов спати? Розрядився.",
    "час": "Годинник ще не підключив, вибач.",
    "погода": "Вікна не бачу, але вір у сонце. ",
    "невідомо": "Я ще вчуся. Спитай про жарт, час чи погоду",
    "привіт": "Привіт-привіт.",
    "музик": "Я не можу слухати музику, але можу розповісти анекдот."
}
JOKES = [
    "Чому робот пішов спати? Розрядився.",
    "Мій улюблений формат - .txt, бо він не сперечається.",
    "Чому робот не може грати в хованки? Бо його завжди знаходять.",
    ]


def answer(theme):
     if theme == "час":
          return datetime.now().strftime("Зараз %H:%M:%S")
     if theme == "жарт":
          return random.choice(JOKES)
     return ANSWERS[theme]

MOOD = random.choice([ "бадьорий", "сонний", "жартівливий"])
PREFIX = {
    "бадьорий": "Ого!",
    "сонний": "Мм...",
    "жартівливий": "Ха!",   
}

while True:
     text = input("Ти: ")
     if text.lower() == "стоп":
          print("ШІ'шка: Бувай!")
          break
     print("ШІ'шка:", PREFIX[MOOD] + " " + answer(analyze(text)))