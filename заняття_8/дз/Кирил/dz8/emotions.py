


EMOTIONS = {
    "дякую": "happy",
    "клас": "happy",
    "помилка": "sad",
    "не працює": "sad",
    "вау": "surprised",
    "цікаво": "thinking",
}


def emotion_for(text):
    text = text.lower()
    for word, emotion in EMOTIONS.items():
        if word in text:
            return emotion

    return "neutral"



print(emotion_for("Дякую, ти класний"))
print(emotion_for("У мене помилка в коді"))
print(emotion_for("вау ось це круто"))
print(emotion_for("Цікаво як це зробити?"))