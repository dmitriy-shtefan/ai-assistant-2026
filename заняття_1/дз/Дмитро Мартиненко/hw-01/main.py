import random
ANSWERS = ["Ти впораєшся!", "Ще трохи!", "Я в тебе вірю.", "Ти сильний!", "Не здавайся!"]
ANSWERS2 = ["Колобок повісився", "Риба втоула", "Змія спіткнулася"]
print ("Привіт! Я ШІ'шка")
print ("Напиши 'СТОП', щоб вийти")
while True:
    text = input("Ти: ")
    if text == "СТОП":
        print("ШІ'шка: Бувай!")
        break
    if text == "мотивуй мене":
        print("ШІ'шка:" + random.choice(ANSWERS))
    elif text == "розкажи анекдот":
        print("ШІ'шка:" + random.choice(ANSWERS2))
    else:
        print("ШІ'шка: Я тебе почув.")