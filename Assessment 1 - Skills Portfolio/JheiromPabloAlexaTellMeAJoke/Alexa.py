import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk, ImageSequence
import random
import os

class JokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa Joke Teller")
        self.root.geometry("650x500")
        self.root.resizable(False, False)

        # Load jokes
        self.jokes = self.load_jokes()

        # Load GIF (optional)
        self.gif_label = tk.Label(root)
        self.gif_label.pack(pady=10)
        self.load_gif()

        # Joke setup label
        self.setup_label = tk.Label(root, text="", font=("Arial", 14), wraplength=550)
        self.setup_label.pack(pady=10)

        # Punchline label
        self.punchline_label = tk.Label(root, text="", font=("Arial", 14, "italic"), fg="blue", wraplength=550)
        self.punchline_label.pack(pady=10)

        # Buttons Frame
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=20)

        # Buttons
        self.tell_button = tk.Button(btn_frame, text="Alexa Tell Me a Joke", width=25, command=self.tell_joke)
        self.tell_button.grid(row=0, column=0, padx=10)

        self.show_button = tk.Button(btn_frame, text="Show Punchline", width=25, state=DISABLED, command=self.show_punchline)
        self.show_button.grid(row=0, column=1, padx=10)

        self.next_button = tk.Button(btn_frame, text="Next Joke", width=25, state=DISABLED, command=self.tell_joke)
        self.next_button.grid(row=1, column=0, pady=10)

        self.quit_button = tk.Button(btn_frame, text="Quit", width=25, command=root.quit)
        self.quit_button.grid(row=1, column=1, pady=10)

        # Storage for current joke
        self.current_setup = ""
        self.current_punchline = ""

    # Load jokes from text file
    def load_jokes(self):
        path = os.path.join("resources", "Assessment 1 - Skills Portfolio/JheiromPabloAlexaTellMeAJoke/randomJokes.txt")

        jokes = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "?" in line:
                    setup, punchline = line.split("?", 1)
                    jokes.append((setup + "?", punchline))
        return jokes

    # Load animated GIF
    def load_gif(self):
        gif_path = os.path.join("resources", "alexa.gif")
        try:
            self.gif = Image.open(gif_path)
            self.frames = [ImageTk.PhotoImage(img.copy().resize((150, 150))) 
                           for img in ImageSequence.Iterator(self.gif)]
            self.gif_index = 0
            self.animate_gif()
        except:
            # If gif missing, show text title instead
            self.gif_label.config(text="Alexa Joke Teller", font=("Arial", 20))

    def animate_gif(self):
        try:
            frame = self.frames[self.gif_index]
            self.gif_label.config(image=frame)
            self.gif_index = (self.gif_index + 1) % len(self.frames)
            self.root.after(80, self.animate_gif)
        except:
            pass

    # Tell a Joke (setup only)
    def tell_joke(self):
        self.current_setup, self.current_punchline = random.choice(self.jokes)
        self.setup_label.config(text=self.current_setup)
        self.punchline_label.config(text="")

        # Activate buttons
        self.show_button.config(state=NORMAL)
        self.next_button.config(state=NORMAL)

    # Show punchline
    def show_punchline(self):
        self.punchline_label.config(text=self.current_punchline)


# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    JokeApp(root)
    root.mainloop()
