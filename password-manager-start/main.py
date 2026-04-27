"""Password Manager Application using Tkinter GUI."""

import json
from tkinter import Tk, Canvas, PhotoImage, Label, Entry, Button, END
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    """Generate a random password and insert it into the password entry field."""
    letters = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
    ]
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    symbols = ["!", "#", "$", "%", "&", "(", ")", "*", "+"]
    password_list = []
    nr_letters = randint(8, 10)
    nr_symbols = randint(2, 4)
    nr_numbers = randint(2, 4)

    # for char in range(nr_letters):
    #     password_list.append(choice(letters))
    password_list = [choice(letters) for char in range(nr_letters)]

    # for char in range(nr_symbols):
    #     password_list += choice(symbols)
    password_list += [choice(symbols) for char in range(nr_symbols)]

    # for char in range(nr_numbers):
    #     password_list += choice(numbers)
    password_list += [choice(numbers) for char in range(nr_numbers)]

    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_password():
    """Save password entry to file and clear the input fields."""
    website_txt = website_entry.get()
    password_txt = password_entry.get()
    username_txt = username_entry.get()
    new_data = {
        website_txt: {
            "email": username_txt,
            "password": password_txt,
        }
    }

    if len(website_txt) == 0:
        messagebox.showerror(title="Error", message="Please input a website.")

    elif len(password_txt) == 0:
        messagebox.showerror(
            title="Error", message="Please input or generate a password."
        )

    elif len(username_txt) == 0:
        messagebox.showerror(title="Error", message="Please input a username or email.")

    else:
        try:
            with open("file.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                data.update(new_data)
        except FileNotFoundError:
            data = new_data
        with open("file.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        website_entry.delete(0, END)
        password_entry.delete(0, END)


def search_password():
    """Search for a password entry in the file and display it."""
    website_txt = website_entry.get()
    try:
        with open("file.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            if website_txt in data:
                messagebox.showinfo(
                    title="Password",
                    message=f"Password: {data[website_txt]['password']}",
                )
            else:
                messagebox.showerror(
                    title="Error", message="No data for that website found."
                )
    except FileNotFoundError:
        messagebox.showerror(title="File Not Found", message="No data file found.")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

website_label = Label(window, text="Website", font=("Arial", 10))
website_label.grid(column=0, row=1)

username_label = Label(window, text="Email/Username:", font=("Arial", 10))
username_label.grid(column=0, row=2)

password_label = Label(window, text="Password:", font=("Arial", 10))
password_label.grid(column=0, row=3)

website_entry = Entry(window, width=16)
website_entry.grid(column=1, row=1)
website_entry.focus()

username_entry = Entry(window, width=36)
username_entry.grid(column=1, row=2, columnspan=2)
username_entry.insert(0, "angus@email.com")

password_entry = Entry(window, width=23)
password_entry.grid(column=1, row=3)

generate_button = Button(
    window, text="Generate Password", command=generate_password, width=13
)
generate_button.grid(column=2, row=3)

save_button = Button(window, text="Add", command=save_password, width=36)
save_button.grid(column=1, row=4, columnspan=2)

search_button = Button(window, text="Search", command=search_password, width=13)
search_button.grid(column=2, row=1)

window.mainloop()
