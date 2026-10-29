import speech_recognition as sr
r = sr.___()                                                    # 1
def listen():
    with sr.Microphone() as mic:
        r.adjust_for_ambient_noise(mic, duration=1)
        print("Говори...")
        audio = r.listen(mic, phrase_time_limit=8)
    try:
        return r.recognize_google(audio, language="___")        # 2
    except sr.UnknownValueError:
        return ___                                              # 3
while True:
    text = ___                                                  # 4
    if text == "":
        ___                                                     # 5
    print("Ти:", text)
    with open("log_speech.txt", "___", encoding="utf-8") as f:  # 6
        f.write(text + "\n")
    if "стоп" ___ text.lower():                                 # 7
        break
    print("АІДА: Я тебе почула.")
