import tkinter as tk
from PIL import Image, ImageTk
from emotions import emotion_for

window = tk.Tk()
window.title("АІДА")
window.geometry("400x520")

pic = Image.open("neutral.png").resize((300, 300))
photo = ImageTk.PhotoImage(pic)

face = tk.Label(window, image=photo)
face.pack(pady=20)
face.image = photo

text = tk.Label(window, text="Привіт! Я АІДА.", font=("Arial", 18))
text.pack()

COLORS = {"happy": "#FFF3C4", "sad": "#D6E4F0",
          "neutral": "#F1EFE8"}

def set_emotion(name):
    pic = Image.open(name + ".png").resize((300, 300))
    photo = ImageTk.PhotoImage(pic)
    face.config(image=photo)
    face.image = photo
    window.configure(bg=COLORS[name])

set_emotion(emotion_for("дякую, ти класна"))

window.mainloop()
