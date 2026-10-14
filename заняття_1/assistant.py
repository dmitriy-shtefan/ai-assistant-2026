import random

ANSWERS = ["Ти впораєшся!", "Ще трохи!", "Я в тебе вірю."]

print("Привіт! Я АІДА. Напиши «стоп», щоб вийти.")

while True:
    text = input("Ти: ")
    if text == "стоп":
        print("АІДА: Бувай!")
        break
    if text == "мотивуй мене":
        print("АІДА: " + random.choice(ANSWERS))
    else:
        print("АІДА: Я тебе почула.")
