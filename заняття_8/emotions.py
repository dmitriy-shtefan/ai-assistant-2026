EMOTIONS = {"дякую": "happy", "клас": "happy",
            "помилка": "sad", "не працює": "sad"}

def emotion_for(text):
    text = text.lower()
    for word, emotion in EMOTIONS.items():
        if word in text:
            return emotion
    return "neutral"

print(emotion_for("дякую, ти класна"))
print(emotion_for("у мене помилка в коді"))
