"""
Blackjack Strategy Flashcard Application

A simple GUI application to learn blackjack basic strategy using flashcards.
Optimized for double-deck games where the dealer hits on soft 17.
"""

import tkinter as tk
from gui import BlackjackFlashcardApp


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('616x560')
    app = BlackjackFlashcardApp(root)
    root.mainloop()
