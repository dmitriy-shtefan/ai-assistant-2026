import requests
KEY = open("key.txt", encoding="utf-8").read().strip()
URL = "https://api.openai.com/v1/chat/completions"
HEAD = {"Authorization": "Bearer " + KEY}
messages = [{"role": "system", "content":
             "Ти ведеш вікторину про космос. Став по одному питанню за раз, "
             "чекай на відповідь, кажи «правильно» чи «ні» і веди рахунок."}]

def ask(text):
    messages.append({"role": "user", "content": text})
    data = {"model": "gpt-6-luna", "messages": messages}
    r = requests.post(URL, headers=HEAD, json=data)
    if r.status_code != 200:
        return "Помилка. Код: " + str(r.status_code)
    answer = r.json()["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": answer})
    return answer

print("Ведучий:", ask("Починаємо вікторину."))
while True:
    q = input("Ти: ")
    if q == "стоп":
        break
    if q == "рахунок":
        print("[у пам'яті]", len(messages), "повідомлень")
        continue
    print("Ведучий:", ask(q))