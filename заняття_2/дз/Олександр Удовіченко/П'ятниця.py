import time
from time import datatime
import random

text = input("Ти: ").lower()

###if "жарт" in text:
###    print("П'ятниця: Чому робот пішов спати? Розрядився.")
###elif "привіт" in text:
###    print("П'ятниця: Привіт-привіт!")
###elif "погод" in text:
###    print("П'ятниця: Вікна не бачу, але вір у сонце")
###else:
###    print("П'ятниця: Я ще вчуся.")
###
def analyze(text):
    text = text.lower()
    if "жарт" in text:
        return "жарт"
    if "час" in text or "годин" in text:
            return "час"
    if "погод" in text:
            return "погода"
    return "невідмо"


print(analyze("Розкажи жарт"))
print(analyze("скільки років черепасі"))


ANSWERS = {
     "жарт": "Чому робот пішов спати? Розрядився.",
     "час": "Годинник, ще не підключив, вибач.",
     "погода": "Вікна не бачу, але вір у сонце.",
     "музик": "Вибач, музику тільки починаю додавати.",
     "невідомо": "Я ще вчусяю. Спитай про жарт, час чи погоду."

}

JOKES = ["Робот пішов спати - розрядився.",
              "Мій улюблений формат - .txt, він не сперечається.", 
              "Робот каже: «Я не втомився». Бо в нього режим енергозбереження!"]

POGODA = ["Для мене вся погода добра.",
          "Вибач я не підключив погоду."]


MOOD = random.choice(["бадьорий","сонний","жартівливий"])
PREFIX = {
     "бадьорий": "Ого! "
     "сонний;" "Мм... "
     "жартівливий:" "Ха! "
}



def answer(tema):
     if tema == "час":
          return datetime.now().strftime("Зараз %H:%M")
     if tema == "жарт":
         return random.choice(JOKES)
     if tema == "погода":
        return random.choice(POGODA)
     return ANSWERS[tema]

    
while True:
     text = input("Ти: ")
     if text.lower() == "стоп":
          print("П'ятниця: Бувай!")
          break
     print("П'ятниця: ", ANSWERS[analyze(text)])


print("П'ятниця: "+ PREFIX[MOOD] + answer(analyze(text)))
    
