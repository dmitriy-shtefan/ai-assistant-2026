import speech_recognition as sr

names = sr.Microphone.list_microphone_names()
print("Мікрофонів знайдено:", len(names))

for i, name in enumerate(names):
    print(i, name)


r = sr.Recognizer()

with sr.Microphone() as mic:
    r.adjust_for_ambient_noise(mic, duration=1)
    print("Говори...")
    audio = r.listen(mic, timeout=5, phrase_time_limit=8)
try:
    text = r.recognize_google(audio, language="uk-UA")
    print("Ти сказав:", text)
except sr.UnknownValueError:
    print("АІДА: Не розчула. Повтори, будь ласка.")
