from tkinter import *  # noqa: F403

window = Tk()  # noqa: F405


def button_clicked():
    my_label.config(text=input.get())


button = Button(window, text="Click Me", command=button_clicked)  # noqa: F405
button.grid(column=1, row=1)
window.title("My First GUI Program")
window.minsize(width=500, height=300)
window.config(padx=20, pady=20)

# Label

my_label = Label(window, text="I Am a Label", font=("Arial", 24, "bold"))  # noqa: F405
my_label["text"] = "New Text"
my_label.config(text="New Text")
my_label.grid(column=0, row=0)

# Entry

input = Entry(window, width=10) # noqa: F405
# print(input.get())
input.grid(column=3, row=2)


# Second Button
def button_clicked2():
    my_label.config(text="New Label")


button2 = Button(window, text="Restart", command=button_clicked2)  # noqa: F405
button2.grid(column=2, row=0)

window.mainloop() 
