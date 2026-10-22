import random

ANSWERS = [
    "Ти зможеш!",
    "Не здавайся, у тебе все вийде!"
]

while True:
    command = input("Напиши команду: ").lower()

    if command == "мотивуй мене":
        print(random.choice(ANSWERS))
    elif command == "підбадьор мене":
        print("Вір у себе!")
    elif command == "вихід":
        print("Бувай!")
        break
    else:
        print("Не знаю такої команди.")