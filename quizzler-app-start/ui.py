from tkinter import Tk, Canvas, Button, Label, PhotoImage
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"


class QuizInterface:
    """Sets up the interface of the Quiz App"""

    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.quiz.score = 0
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
            text="Score: 0",
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
        """fetches the next question"""
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.canvas.itemconfig(self.question_text, text="You've reached the end of the quiz!")
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")

    def check_true(self):
        """checks if the user's answer is correct"""
        is_right = self.quiz.check_answer("true")
        self.give_feedback(is_right)
    
    def check_false(self):
        """user clicks the false button"""
        is_right = self.quiz.check_answer("false")
        self.give_feedback(is_right)

    def give_feedback(self, is_right):
        """user clicks the true button"""
        if is_right:
            self.score_label.config(text=f"Score: {self.quiz.score}")
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        self.window.after(1000, self.get_next_question)

