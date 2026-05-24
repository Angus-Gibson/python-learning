import random
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"

# UI Setup
window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
finally:
    data_dict = data.to_dict(orient="records")

current_word = {}
words_to_learn = [word for word in data_dict]
flip_timer = None

def flip_card():
    canvas.itemconfig(card_img, image=card_back_img)
    canvas.itemconfig(card_title, text="English")
    canvas.itemconfig(card_word, text=current_word["English"], fill="white")


def new_card():
    global current_word, flip_timer
    if flip_timer is not None:
        window.after_cancel(flip_timer)
    current_word = random.choice(data_dict)
    canvas.itemconfig(card_img, image=card_front_img)
    canvas.itemconfig(card_title, text="French")
    canvas.itemconfig(card_word, text=current_word["French"], fill="black")
    flip_timer = window.after(3000, func=flip_card)

def remove_card():
    words_to_learn.remove(current_word)
    pandas.DataFrame(words_to_learn).to_csv("data/words_to_learn.csv", index=False)
    new_card()

canvas = Canvas(
    width=800,
    height=526,
    bg=BACKGROUND_COLOR,
    highlightthickness=0,
)
card_front_img = PhotoImage(file="images/card_front.png")
card_img = canvas.create_image(400, 263, image=card_front_img)
canvas.grid(column=0, row=0, columnspan=2)

card_back_img = PhotoImage(file="images/card_back.png")

card_title = canvas.create_text(
    400, 150,
    text="French",
    font=("Ariel", 40, "italic"),
)

card_word = canvas.create_text(
        400, 263,
        font=("Ariel", 60, "bold"),
    )

check_button_img = PhotoImage(file="images/right.png")
check_button = Button(
    image=check_button_img,
    highlightthickness=0,
    command=remove_card,
)
check_button.grid(column=1, row=1)

cross_button_img = PhotoImage(file="images/wrong.png")
cross_button = Button(
    image=cross_button_img,
    highlightthickness=0,
    command=new_card,
)
cross_button.grid(column=0, row=1)

new_card()

window.mainloop()



