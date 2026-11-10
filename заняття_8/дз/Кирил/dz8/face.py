import tkinter as tk
from PIL import Image, ImageTk
from emotions import emotion_for

window = tk.Tk()
window.title("S1tx")
window.geometry("400x520")

pic = Image.open("neutral.png").resize((300, 300))
photo = ImageTk.PhotoImage(pic)

face = tk.Label(window, image=photo)
face.pack(pady=20)
face.image = photo

text = tk.Label(window, text="Привіт! Я S1tx.", font=("Arial", 18))
text.pack()

COLORS = {"happy": "#FAC800", "sad": "#1100FF", "neutral": "#F30000",
          "thinking": "#12C438", "surprised": "#DF29F7"}

def set_emotion(name):
    pic = Image.open(name + ".png").resize((300,300))
    photo = ImageTk.PhotoImage(pic)
    face.config(image=photo)
    face.image = photo
    window.configure(bg=COLORS[name])

set_emotion(emotion_for("цікаво"))

window.mainloop()