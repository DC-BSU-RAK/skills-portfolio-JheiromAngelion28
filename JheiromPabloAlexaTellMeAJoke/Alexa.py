import os
import random
import customtkinter as ctk
import tkinter as tk
from tkvideo import tkvideo

# ----------------------------
# Configuration
# ----------------------------
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

# Base directory of this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# File paths
JOKES_PATH = os.path.join(BASE_DIR, "randomJokes.txt")
VIDEO_PATH = os.path.join(BASE_DIR, "Jheirom.mp4")  # Your MP4 video

# ----------------------------
# Helpers
# ----------------------------
def load_jokes(path=JOKES_PATH):
    jokes = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if "?" in line:
                    s, p = line.split("?", 1)
                    jokes.append((s.strip() + "?", p.strip()))
                else:
                    jokes.append((line, ""))
    except Exception:
        # Default jokes if file not found
        jokes = [
            ("Why don't scientists trust atoms?", "Because they make up everything."),
            ("What do you call fake spaghetti?", "An impasta."),
            ("Why did the scarecrow win an award?", "Because he was outstanding in his field."),
            ("What happens if you boil a clown?", "You get a laughing stock."),
            ("Why did the chicken cross the road?", "To get to the other side."),
        ]

    if not jokes:
        jokes = [("No jokes found.", "Add jokes to randomJokes.txt.")]
    return jokes

# ----------------------------
# App
# ----------------------------
class AlexaJokeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Alexa Tell Me A Joke")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Background color fallback
        self.configure(fg_color="#1a1a1a")

        # Load jokes
        self.jokes = load_jokes()
        self.total = len(self.jokes)
        self.current_joke = None

        # Build layout first
        self._build_layout()

        # Load video last (behind widgets)
        self._load_video()

    # ----------------------------
    # Layout
    # ----------------------------
    def _build_layout(self):
        # ---- Joke Display Box ----
        joke_frame = ctk.CTkFrame(self, fg_color="transparent", width=900, height=250)
        joke_frame.place(relx=0.5, y=320, anchor="center")

        self.joke_text_label = ctk.CTkLabel(
            joke_frame,
            text="Press 'Alexa Tell me a joke' to start",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#FFFFFF",
            wraplength=850,
            justify="center",
            fg_color="transparent"  # Transparent background
        )
        self.joke_text_label.pack(expand=True)

        # ---- Buttons ----
        y = 480
        btn_colors = ("#1a4d4d", "#0d2626")
        hover_colors = ("#2a6d6d", "#1a3a3a")

        self.show_btn = ctk.CTkButton(
            self, text="Show Punch Line", width=200, height=50,
            corner_radius=10,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color=btn_colors,
            text_color="#FFFFFF",
            border_width=0,  # Remove edges
            hover_color=hover_colors,
            command=self.show_punchline,
            state="disabled"
        )
        self.show_btn.place(x=50, y=y)

        self.tell_btn = ctk.CTkButton(
            self, text="Alexa Tell me a joke", width=280, height=50,
            corner_radius=10,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color=btn_colors,
            text_color="#FFFFFF",
            border_width=0,
            hover_color=hover_colors,
            command=self.tell_joke
        )
        self.tell_btn.place(relx=0.5, y=y, anchor="center")

        self.next_btn = ctk.CTkButton(
            self, text="Next Joke", width=200, height=50,
            corner_radius=10,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color=btn_colors,
            text_color="#FFFFFF",
            border_width=0,
            hover_color=hover_colors,
            command=self.next_joke,
            state="disabled"
        )
        self.next_btn.place(x=750, y=y)

        # ---- Counter + Quit ----
        info_y = 550
        self.counter_label = ctk.CTkLabel(
            self, text=f"Joke 0/{self.total}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FFFFFF",
            fg_color="transparent"
        )
        self.counter_label.place(x=50, y=info_y)

        self.quit_btn = ctk.CTkButton(
            self, text="QUIT", width=150, height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color=("#4d1a1a", "#330d0d"),
            text_color="#FFFFFF",
            border_width=0,
            hover_color=("#6d2a2a", "#4d1a1a"),
            command=self.quit_app
        )
        self.quit_btn.place(relx=0.5, y=info_y, anchor="center")

    # ----------------------------
    # Video Background
    # ----------------------------
    def _load_video(self):
        """Load MP4 video and send to background"""
        try:
            if not os.path.exists(VIDEO_PATH):
                print(f"Video not found at: {VIDEO_PATH}")
                return

            self.video_label = tk.Label(self, bg="#1a1a1a")
            self.video_label.place(x=0, y=0, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
            self.video_label.lower()  # send to back

            self.video_player = tkvideo(
                VIDEO_PATH,
                self.video_label,
                loop=1,
                size=(WINDOW_WIDTH, WINDOW_HEIGHT)
            )
            self.video_player.play()

            print("Video loaded and playing!")

        except Exception as e:
            print(f"Error loading video: {e}")

    # ----------------------------
    # Joke Logic
    # ----------------------------
    def tell_joke(self):
        if not self.jokes:
            return

        self.current_joke = random.choice(self.jokes)
        setup, _ = self.current_joke

        self.joke_text_label.configure(text=setup)
        self.show_btn.configure(state="normal")
        self.next_btn.configure(state="normal")

        index = self.jokes.index(self.current_joke) + 1
        self.counter_label.configure(text=f"Joke {index}/{self.total}")

    def show_punchline(self):
        if not self.current_joke:
            return
        setup, punchline = self.current_joke
        self.joke_text_label.configure(text=f"{setup}\n\n{punchline}")
        self.show_btn.configure(state="disabled")

    def next_joke(self):
        self.tell_joke()

    def quit_app(self):
        self.destroy()


# ----------------------------
# Run App
# ----------------------------
if __name__ == "__main__":
    app = AlexaJokeApp()
    app.mainloop()
