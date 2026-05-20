BACKGROUND_COLOR = "#B1DDC6"
from tkinter import *
from random import *

#UI Setup
window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
canvas.create_image(400, 263, image=card_front_img)
canvas.grid(column=0, row=0, columnspan=2)

french_label = Label(text="French",
                     font=("Ariel", 40, "italic"),
                     fg="black", highlightthickness=0, bg="white"
)
french_label.place(x=400, y=150, anchor="center")

check_button_img = PhotoImage(
    file="images/right.png"
)
check_button = Button(image=check_button_img, highlightthickness=0)
check_button.grid(column=1, row=1)

cross_button_img = PhotoImage(
    file="images/wrong.png"
)
cross_button = Button(image=cross_button_img, highlightthickness=0)
cross_button.grid(column=0, row=1)

window.mainloop()
