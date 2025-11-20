import tkinter as tk
from tkinter import *
import random
import os

class JokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa Joke Teller")
        self.root.geometry("900x550")
        self.root.resizable(False, False)
        self.root.configure(bg="#4b1cd4")   # Modern purple background

        # Load jokes
        self.jokes = self.load_jokes()

        # Main Frame (center everything)
        self.main_frame = Frame(root, bg="#4b1cd4")
        self.main_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Rounded container for joke text
        self.joke_frame = Frame(self.main_frame, bg="#777777")
        self.joke_frame.pack(pady=20)

        # Joke setup label
        self.setup_label = Label(
            self.joke_frame,
            text="",
            bg="#777777",
            fg="white",
            font=("Arial", 18),
            wraplength=700,
            justify="center",
            pady=20
        )
        self.setup_label.pack()

        # Punchline label
        self.punchline_label = Label(
            self.joke_frame,
            text="",
            bg="#777777",
            fg="black",
            font=("Arial", 18, "italic"),
            wraplength=700,
            justify="center",
            pady=20
        )
        self.punchline_label.pack()

        # Buttons Frame
        self.btn_frame = Frame(self.main_frame, bg="#4b1cd4")
        self.btn_frame.pack(pady=20)

        # Modern Button Style
        btn_style = {
            "width": 20,
            "height": 2,
            "font": ("Arial", 14, "bold"),
            "bg": "#777777",
            "fg": "white",
            "activebackground": "#5e5e5e",
            "relief": "flat",
            "bd": 0
        }

        # Buttons
        self.tell_button = Button(
            self.btn_frame, text="Alexa Tell Me a Joke",
            command=self.tell_joke, **btn_style
        )
        self.tell_button.grid(row=0, column=0, padx=10, pady=10)

        self.show_button = Button(
            self.btn_frame, text="Show Punchline", state=DISABLED,
            command=self.show_punchline, **btn_style
        )
        self.show_button.grid(row=0, column=1, padx=10, pady=10)

        self.next_button = Button(
            self.btn_frame, text="Next Joke", state=DISABLED,
            command=self.tell_joke, **btn_style
        )
        self.next_button.grid(row=1, column=0, padx=10, pady=10)

        self.quit_button = Button(
            self.btn_frame, text="Quit", command=root.quit, **btn_style
        )
        self.quit_button.grid(row=1, column=1, padx=10, pady=10)

        # Store current joke
        self.current_setup = ""
        self.current_punchline = ""

    # ------------------------------------
    # Load jokes from randomJokex.txt
    # ------------------------------------
    def load_jokes(self):
        path = "JheiromPabloAlexaTellMeAJoke/randomJokes.txt"  # same folder as script
        jokes = []

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "?" in line:
                    setup, punchline = line.split("?", 1)
                    jokes.append((setup + "?", punchline))

        return jokes

    # ------------------------------------

    def tell_joke(self):
        self.current_setup, self.current_punchline = random.choice(self.jokes)

        self.setup_label.config(text=self.current_setup)
        self.punchline_label.config(text="")

        self.show_button.config(state=NORMAL)
        self.next_button.config(state=NORMAL)

    def show_punchline(self):
        self.punchline_label.config(text=self.current_punchline)


# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    JokeApp(root)
    root.mainloop()
