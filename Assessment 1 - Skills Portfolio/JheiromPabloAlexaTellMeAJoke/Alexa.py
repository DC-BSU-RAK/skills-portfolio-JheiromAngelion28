import tkinter as tk
from tkinter import messagebox
import random
import os
from PIL import Image, ImageTk


class JokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa - Tell Me A Joke!")
        self.root.geometry("600x450")
        self.root.resizable(False, False)

        # Load jokes
        self.jokes = self.load_jokes()

        # Load Image
        self.alexa_img = None
        self.load_image()

        # UI Layout
        self.create_widgets()

    # -----------------------------
    # LOAD JOKES (NO RESOURCES FOLDER)
    # -----------------------------
    def load_jokes(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, "randomJokes.txt")

        if not os.path.exists(path):
            print(f"Joke file not found: {path}")
            return ["Error: randomJokes.txt not found."]

        with open(path, "r", encoding="utf-8") as f:
            jokes = [line.strip() for line in f if line.strip()]

        return jokes

    # -----------------------------
    # LOAD IMAGE (OPTIONAL)
    # -----------------------------
    def load_image(self):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            img_path = os.path.join(base_dir, "alexa.png")  # Optional image file

            if os.path.exists(img_path):
                img = Image.open(img_path)
                img = img.resize((250, 250))
                self.alexa_img = ImageTk.PhotoImage(img)
        except:
            self.alexa_img = None

    # -----------------------------
    # UI SETUP
    # -----------------------------
    def create_widgets(self):

        # Alexa Picture
        if self.alexa_img:
            self.img_label = tk.Label(self.root, image=self.alexa_img)
            self.img_label.pack(pady=10)
        else:
            tk.Label(self.root, text="Alexa Joke Machine", font=("Arial", 18, "bold")).pack(pady=10)

        # Joke Display Box
        self.joke_box = tk.Text(self.root, height=5, width=50, wrap=tk.WORD, font=("Arial", 12))
        self.joke_box.pack(pady=15)

        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack()

        self.joke_button = tk.Button(
            button_frame, text="Tell Me a Joke",
            font=("Arial", 14), width=20,
            command=self.show_joke
        )
        self.joke_button.grid(row=0, column=0, padx=10)

        self.clear_button = tk.Button(
            button_frame, text="Clear",
            font=("Arial", 14), width=10,
            command=self.clear_joke
        )
        self.clear_button.grid(row=0, column=1, padx=10)

    # -----------------------------
    # SHOW RANDOM JOKE
    # -----------------------------
    def show_joke(self):
        if not self.jokes:
            messagebox.showerror("Error", "No jokes found.")
            return

        joke = random.choice(self.jokes)
        self.joke_box.delete(1.0, tk.END)
        self.joke_box.insert(tk.END, joke)

    # -----------------------------
    # CLEAR JOKE BOX
    # -----------------------------
    def clear_joke(self):
        self.joke_box.delete(1.0, tk.END)


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    JokeApp(root)
    root.mainloop()
