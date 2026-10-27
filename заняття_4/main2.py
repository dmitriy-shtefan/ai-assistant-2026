import requests

with open("key.txt", encoding="utf-8") as f:
    KEY = f.read().strip()

URL = "https://api.openai.com/v1/chat/completions"
headers = {"Authorization": "Bearer " + KEY}
data = {"model": "gpt-6-luna",
        "messages": [{"role": "user", "content": "Привіт! Хто ти?"}]}

r = requests.post(URL, headers=headers, json=data)
print("Код:", r.status_code)
