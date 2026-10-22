import random

# Відповіді бота
ANSWERS = {
    "мотивуй мене": "Ти зможеш!",
    "підбадьор мене": "Вір у себе!",
    "музика": "Увімкни улюблену пісню та відпочинь!"
}

# Жарти бота
JOKES = [
    "Чому книжка сумувала? Бо в неї було забагато проблем.",
    "Що каже комп'ютер, коли змерз? Закрий вікно!",
    "Чому музика не спізнюється? Бо завжди йде в такт!"
]

# Аналіз повідомлень
def analyze(message):
    message = message.lower()

    if "погода" in message:
        return "погода"
    elif "музика" in message:
        return "музика"
    elif "жарт" in message:
        return "жарт"
    return message

while True:
    command = input("Напиши команду: ").strip().lower()

    if command == "вихід":
        print("Бувай!")
        break

    result = analyze(command)

    if result in ANSWERS:
        print(ANSWERS[result])
    elif result == "жарт":
        print(random.choice(JOKES))
    else:
        print("Не знаю такої команди.")
