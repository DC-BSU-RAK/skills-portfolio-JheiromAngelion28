import tkinter as tk
from tkinter import *
import random
import os
import time

class JokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa Joke Teller")
        self.root.geometry("900x550")
        self.root.resizable(False, False)

        # ---------------------------
        # Gradient Background Canvas
        # ---------------------------
        self.canvas = tk.Canvas(root, width=900, height=550, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.draw_gradient("#5728ff", "#3f0fae")

        # Main container frame (centered)
        self.main_frame = Frame(root, bg="", highlightthickness=0)
        self.main_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Load jokes
        self.jokes = self.load_jokes()

        # ---------------------------
        # Modern Rounded Card Background
        # ---------------------------
        self.card = Frame(self.main_frame, bg="#6b6b6b", bd=0)
        self.card.pack(pady=25)

        # Joke setup
        self.setup_label = Label(
            self.card,
            text="",
            bg="#6b6b6b",
            fg="white",
            font=("Segoe UI", 20),
            wraplength=700,
            pady=20,
            justify="center"
        )
        self.setup_label.pack()

        # Punchline
        self.punchline_label = Label(
            self.card,
            text="",
            bg="#6b6b6b",
            fg="#f1f1f1",
            font=("Segoe UI", 20, "italic"),
            wraplength=700,
            pady=20,
            justify="center"
        )
        self.punchline_label.pack()

        # Buttons frame
        btn_frame = Frame(self.main_frame, bg="", highlightthickness=0)
        btn_frame.pack(pady=20)

        # Glow button style
        self.btn_style = {
            "width": 18,
            "height": 2,
            "font": ("Segoe UI", 14, "bold"),
            "bg": "#6b6b6b",
            "fg": "white",
            "activebackground": "#5e5e5e",
            "relief": "flat",
            "bd": 0
        }

        # Buttons
        self.tell_button = self.create_glow_button(btn_frame, "Alexa Tell Me a Joke", self.tell_joke)
        self.tell_button.grid(row=0, column=0, padx=10, pady=10)

        self.show_button = self.create_glow_button(btn_frame, "Show Punchline", self.show_punchline)
        self.show_button.grid(row=0, column=1, padx=10, pady=10)
        self.show_button.config(state=DISABLED)

        self.next_button = self.create_glow_button(btn_frame, "Next Joke", self.tell_joke)
        self.next_button.grid(row=1, column=0, padx=10, pady=10)
        self.next_button.config(state=DISABLED)

        self.quit_button = self.create_glow_button(btn_frame, "Quit", root.quit)
        self.quit_button.grid(row=1, column=1, padx=10, pady=10)

        # Storage
        self.current_setup = ""
        self.current_punchline = ""

    # ---------------------------
    # Gradient Background Drawing
    # ---------------------------
    def draw_gradient(self, color1, color2):
        for i in range(550):
            r1, g1, b1 = self.hex_to_rgb(color1)
            r2, g2, b2 = self.hex_to_rgb(color2)
            ratio = i / 550
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            line_color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_line(0, i, 900, i, fill=line_color)

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    # ---------------------------
    # Glow Button Creator
    # ---------------------------
    def create_glow_button(self, parent, text, command):
        btn = Button(parent, text=text, command=command, **self.btn_style)

        # Hover effect
        def on_enter(e):
            btn.config(bg="#8a8a8a")
        def on_leave(e):
            btn.config(bg="#6b6b6b")

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        return btn

    # ---------------------------
    # Load jokes
    # ---------------------------
    def load_jokes(self):
        path = "JheiromPabloAlexaTellMeAJoke/randomJokes.txt"
        jokes = []

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "?" in line:
                    setup, punchline = line.split("?", 1)
                    jokes.append((setup + "?", punchline))

        return jokes

    # ---------------------------
    # Show setup
    # ---------------------------
    def tell_joke(self):
        self.current_setup, self.current_punchline = random.choice(self.jokes)
        self.setup_label.config(text=self.current_setup)
        self.punchline_label.config(text="")

        self.show_button.config(state=NORMAL)
        self.next_button.config(state=NORMAL)

    # ---------------------------
    # Smooth fade-in punchline
    # ---------------------------
    def show_punchline(self):
        text = self.current_punchline
        self.punchline_label.config(text="")

        # Fade-in animation
        for i in range(1, len(text) + 1):
            self.punchline_label.config(text=text[:i])
            self.root.update()
            time.sleep(0.02)


# Run App
if __name__ == "__main__":
    root = tk.Tk()
    JokeApp(root)
    root.mainloop()
