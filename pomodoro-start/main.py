from tkinter import Label, Button, Tk, Canvas, PhotoImage
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global reps, timer
    window.after_cancel(timer)
    timer = None
    timer_label.config(text="Timer", fg=GREEN)
    checkmarks.config(text="")
    canvas.itemconfig(timer_text, text="00:00")
    reps = 0


# --------------------------- TIMER MECHANISM --------------------------- #
def start_timer():
    if timer is not None:
        return
    global reps
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
    reps += 1

    if reps % 8 == 0:
        timer_label.config(text="Break", fg=RED)
        countdown(long_break_sec)

    elif reps % 2 != 0:
        timer_label.config(text="Work", fg=GREEN)
        countdown(work_sec)
    # If it's the 2nd/4th/6th rep:
    else:
        timer_label.config(text="Break", fg=PINK)
        countdown(short_break_sec)


# ------------------- COUNTDOWN MECHANISM --------------------------- #
def countdown(count):

    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, countdown, count - 1)
    else:
        start_timer()
        marks = ""
        for _ in range(math.floor(reps / 2)):
            marks += "✔"
        checkmarks.config(text=marks)


# -------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

# Timer label

timer_label = Label(
    window,
    text="Timer",
    font=(FONT_NAME, 50),
    fg=GREEN,
    bg=YELLOW,
    highlightthickness=0,
)
timer_label.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(
    105, 130, text="00:00", fill="white", font=(FONT_NAME, 30, "bold")
)
canvas.grid(column=1, row=1)

# start button

start_button = Button(window, text="Start", command=start_timer, highlightthickness=0)
start_button.grid(column=0, row=2)

# reset timer

reset_button = Button(window, text="Reset", command=reset_timer, highlightthickness=0)
reset_button.grid(column=2, row=2)

checkmarks = Label(window, font=(30), fg=GREEN, bg=YELLOW, highlightthickness=0)
checkmarks.grid(column=1, row=3)


window.mainloop()
