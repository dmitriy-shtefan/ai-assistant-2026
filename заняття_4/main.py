import requests

with open("key.txt", encoding="utf-8") as f:
    KEY = f.read().strip()

URL = "https://api.openai.com/v1/chat/completions"
headers = {"Authorization": "Bearer " + KEY}

def ask_ai(question):
    data = {"model": "gpt-6-luna",
            "messages": [{"role": "user", "content": question}]}
    r = requests.post(URL, headers=headers, json=data)
    if r.status_code != 200:
        return "Не вийшло спитати. Код: " + str(r.status_code)
    return r.json()["choices"][0]["message"]["content"]

def ask_ai_mock(question):
    return "Я зараз без мережі, але уяви, що я відповів."

while True:
    text = input("Ти: ")
    if text.lower() == "стоп":
        break
    print("АІДА:", ask_ai(text))
