from tkinter import *
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"


class QuizInterface:
    """Sets up the interface of the Quiz App"""

    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, background=THEME_COLOR)

        self.canvas = Canvas(
            width=300, height=250, background="white", highlightthickness=0
        )
        self.canvas.grid(column=0, row=1, columnspan=2, pady=20, padx=20)
        self.question_text = self.canvas.create_text(
            150,
            125,
            width=280,
            text="Questions go here",
            fill="black",
            font=("arial", 20, "italic"),
        )

        self.score_label = Label(
            text=f"Score: {self.quiz.score}",
            font=("arial", 10),
            fg="white",
            bg=THEME_COLOR,
            highlightthickness=0,
        )
        self.score_label.grid(column=1, row=0)

        self.true_img = PhotoImage(file="images/true.png")
        self.true_button = Button(
            image=self.true_img,
            highlightthickness=0,
            command=self.check_true
        )
        self.true_button.grid(column=0, row=2)

        self.false_img = PhotoImage(file="images/false.png")
        self.false_button = Button(
            image=self.false_img,
            highlightthickness=0,
            command=self.check_false
        )
        self.false_button.grid(column=1, row=2)

        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        self.canvas.config(bg="white")
        q_text = self.quiz.next_question()
        self.canvas.itemconfig(self.question_text, text=q_text)

    def check_true(self):
        is_right = self.quiz.check_answer("true")
        self.give_feedback(is_right)
    
    def check_false(self):
        is_right = self.quiz.check_answer("false")
        self.give_feedback(is_right)

    def give_feedback(self, is_right):
        if is_right:
            self.quiz.score += 1
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        self.window.after(1000, self.get_next_question)

