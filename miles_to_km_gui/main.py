from tkinter import Tk, Entry, Label, Button

window = Tk()
window.title("Mile to Km Converter")
window.minsize(width=200, height=100)
window.config(padx=20, pady=20)

miles_input = Entry(window, width=10, justify="center")
miles_input.grid(column=1, row=0)

miles_label = Label(window, text="Miles", font=("Arial", 16))
miles_label.grid(column=2, row=0)

is_equal_to = Label(window, text="is equal to", font=("Arial", 16))
is_equal_to.grid(column=0, row=1)

current_km = Label(window, text="0", font=("Arial", 16))
current_km.grid(column=1, row=1)

km_label = Label(window, text="Km", font=("Arial", 16))
km_label.grid(column=2, row=1)


def convert():
    miles = float(miles_input.get())
    km = miles * 1.60934
    current_km.config(text=f"{km:.3f}")


button = Button(window, text="Calculate", command=convert)
button.grid(column=1, row=2)

window.mainloop()

