from gtts import gTTS
from playsound import playsound

gTTS("Мене чути?", lang="uk").save("test.mp3")
playsound("test.mp3")
print("Дограло")
