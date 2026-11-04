import requests

KEY = open("key.txt", encoding="utf-8").read().strip()
URL = "https://api.openai.com/v1/chat/completions"
HEADER = {"Authorization": f"Bearer {KEY}",}

def ask_ai(question):
    data = {"model": "gpt-6-luna", "messages": [{"role": "user", "content": question}]}
    r = requests.post(URL, headers=HEADER, json=data)
    if r.status_code != 200:
        return "Помилка. Код: " + str(r.status_code)
    return r.json()["choices"][0]["message"]["content"]
