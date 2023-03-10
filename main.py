from tkinter import *
import random
import pandas
import time
TIMER = 3000

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("sprak.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="Tyska", fill="black")
    canvas.itemconfig(card_word, text=current_card["Tyska"], fill="black")
    canvas.itemconfig(card_background, image=card_front_image)
    flip_timer = window.after(TIMER, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="Svenska", fill="white")
    canvas.itemconfig(card_word, text=current_card["Svenska"], fill="white")
    canvas.itemconfig(card_background, image=card_back_image)

def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flash")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(TIMER, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_image)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "italic"))

canvas.grid(row=0, column=0, columnspan=2)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)


# Button
cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image)
unknown_button.grid(row=1, column=0)
unknown_button.config(bg=BACKGROUND_COLOR, highlightthickness=0, command=next_card)

check_image = PhotoImage(file="images/right.png")
know_button = Button(image=check_image)
know_button.grid(row=1, column=1)
know_button.config(bg=BACKGROUND_COLOR, highlightthickness=0, command=is_known)

next_card()

window.mainloop()
