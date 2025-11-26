import os
import random
import customtkinter as ctk
from PIL import Image, ImageTk

# ----------------------------
# Configuration
# ----------------------------
WINDOW_WIDTH = 980
WINDOW_HEIGHT = 620
JOKES_PATH = os.path.join(os.path.dirname(__file__), "randomJokes.txt")
GIF_PATH = os.path.join(os.path.dirname(__file__), "JheiromPabloAlexaTellMeAJoke/Alexa.py")

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
                    setup, punch = line.split("?", 1)
                    jokes.append((setup.strip() + "?", punch.strip()))
                else:
                    jokes.append((line, ""))
    except Exception:
        jokes = [
            ("Why don't scientists trust atoms?", "Because they make up everything."),
            ("What do you call fake spaghetti?", "An impasta."),
            ("Why did the scarecrow win an award?", "Because he was outstanding in his field."),
        ]

    if not jokes:
        jokes = [("No jokes found.", "Add jokes to randomJokes.txt.")]
    return jokes

# ----------------------------
# Ultra Modern App
# ----------------------------
class UltraModernJokeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Alexa — Ultra Modern Joke Teller")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.jokes = load_jokes()
        self.total = len(self.jokes)
        self.current_index = None
        self.revealing = False

        # GIF state
        self.gif_frames = []
        self.gif_index = 0

        # Card animation state
        self._neon_phase = 0
        self._neon_dir = 1
        self._card_base_y = 60
        self._card_float_offset = 0
        self._card_float_dir = 1

        self._build_layout()
        self._load_gif()
        self._animate_gif()
        self._neon_step()
        self._card_float_animation()
        self._show_welcome()

    # ----------------------------
    # Layout building
    # ----------------------------
    def _build_layout(self):
        # -----------------
        # Full-screen GIF background
        # -----------------
        self.gif_label = ctk.CTkLabel(self, text="", width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.gif_label.place(x=0, y=0)
        self.gif_label.lower()  # send to back

        # -----------------
        # Title
        # -----------------
        self.title_label = ctk.CTkLabel(self, text="Alexa — Ultra Modern Joke Teller",
                                        font=ctk.CTkFont(size=28, weight="bold"), text_color="white")
        self.title_label.place(relx=0.5, y=20, anchor="n")

        # -----------------
        # Joke Card
        # -----------------
        card_w, card_h = 620, 420
        card_x = (WINDOW_WIDTH - card_w) // 2
        card_y = self._card_base_y

        self.card_shadow = ctk.CTkFrame(self, corner_radius=28,
                                        fg_color="#071022", width=card_w, height=card_h)
        self.card_shadow.place(x=card_x + 8, y=card_y + 8)

        # Fixed: Removed alpha channel from color
        self.card = ctk.CTkFrame(self, corner_radius=28, fg_color="#0e1220",
                                 border_width=2, border_color="#3a6cff",
                                 width=card_w, height=card_h)
        self.card.place(x=card_x, y=card_y)

        # Top row
        top_row = ctk.CTkFrame(self.card, fg_color="transparent")
        top_row.pack(padx=22, pady=(18, 6), fill="x")
        ctk.CTkLabel(top_row, text="Joke Mode", font=ctk.CTkFont(size=22, weight="bold")).pack(side="left")

        # Joke Frame
        self.joke_frame = ctk.CTkFrame(self.card, corner_radius=16, fg_color="#081323")
        self.joke_frame.pack(padx=18, pady=12, fill="both", expand=True)

        self.setup_label = ctk.CTkLabel(self.joke_frame, text="", wraplength=440,
                                        justify="center", font=ctk.CTkFont(size=18))
        self.setup_label.place(relx=0.5, rely=0.35, anchor="center")

        self.punch_label = ctk.CTkLabel(self.joke_frame, text="", wraplength=440,
                                        justify="center", font=ctk.CTkFont(size=18, slant="italic"))
        self.punch_label.place(relx=0.5, rely=0.6, anchor="center")

        # Bottom Buttons
        bottom = ctk.CTkFrame(self.card, fg_color="transparent")
        bottom.pack(padx=22, pady=(6, 18), fill="x")

        self.counter_label = ctk.CTkLabel(bottom, text="Joke 0 / 0")
        self.counter_label.pack(side="left")

        btn_frame = ctk.CTkFrame(bottom, fg_color="transparent")
        btn_frame.pack(side="right")

        self.tell_btn = ctk.CTkButton(btn_frame, text="Alexa Tell Me a Joke",
                                      width=220, height=40, corner_radius=20,
                                      fg_color="#0e74c7", hover_color="#1290ff",
                                      command=self.tell_joke)
        self.tell_btn.grid(row=0, column=0, padx=10)

        self.show_btn = ctk.CTkButton(btn_frame, text="Show Punchline",
                                      width=160, height=40, corner_radius=20,
                                      fg_color="#263444", hover_color="#2f4f66",
                                      command=self.show_punchline,
                                      state="disabled")
        self.show_btn.grid(row=0, column=1, padx=10)

        self.next_btn = ctk.CTkButton(btn_frame, text="Next",
                                      width=100, height=40, corner_radius=20,
                                      fg_color="#263444", hover_color="#2f4f66",
                                      command=self.tell_joke,
                                      state="disabled")
        self.next_btn.grid(row=0, column=2, padx=10)

    # ----------------------------
    # GIF Loading
    # ----------------------------
    def _load_gif(self):
        try:
            gif = Image.open(GIF_PATH)
            self.gif_frames = []
            frame_count = getattr(gif, "n_frames", 1)
            for i in range(frame_count):
                gif.seek(i)
                frame = gif.convert("RGBA").resize((WINDOW_WIDTH, WINDOW_HEIGHT), Image.LANCZOS)
                overlay = Image.new("RGBA", frame.size, (0, 0, 0, 80))
                frame = Image.alpha_composite(frame, overlay)
                self.gif_frames.append(ImageTk.PhotoImage(frame))
        except Exception as e:
            print("GIF load error:", e)
            self.gif_frames = []

    # ----------------------------
    # GIF Animate
    # ----------------------------
    def _animate_gif(self):
        if self.gif_frames:
            frame = self.gif_frames[self.gif_index]
            self.gif_label.configure(image=frame)
            self.gif_index = (self.gif_index + 1) % len(self.gif_frames)
        self.after(70, self._animate_gif)

    # ----------------------------
    # Neon Animation for card border
    # ----------------------------
    def _neon_step(self):
        phase = (self._neon_phase % 100) / 100
        ca = (48, 118, 255)
        cb = (111, 180, 255)
        r = int(ca[0] + (cb[0] - ca[0]) * phase)
        g = int(ca[1] + (cb[1] - ca[1]) * phase)
        b = int(ca[2] + (cb[2] - ca[2]) * phase)
        self.card.configure(border_color=f"#{r:02x}{g:02x}{b:02x}")
        self._neon_phase += self._neon_dir * 1.8
        if self._neon_phase >= 100 or self._neon_phase <= 0:
            self._neon_dir *= -1
        self.after(50, self._neon_step)

    # ----------------------------
    # Floating card animation
    # ----------------------------
    def _card_float_animation(self):
        self._card_float_offset += self._card_float_dir
        if abs(self._card_float_offset) > 6:
            self._card_float_dir *= -1
        new_y = self._card_base_y + self._card_float_offset
        self.card.place_configure(y=new_y)
        self.card_shadow.place_configure(y=new_y + 8)
        self.after(160, self._card_float_animation)

    # ----------------------------
    # Joke Logic
    # ----------------------------
    def _show_welcome(self):
        self.setup_label.configure(text="Press 'Alexa Tell Me a Joke'")
        self.punch_label.configure(text="")
        self.counter_label.configure(text=f"Joke 0 / {self.total}")

    def tell_joke(self):
        if not self.jokes:
            return
        new_index = random.randrange(len(self.jokes))
        self.current_index = new_index
        setup, punch = self.jokes[new_index]
        self.current_setup = setup
        self.current_punch = punch
        self._type_setup(setup)
        self.punch_label.configure(text="")
        self.show_btn.configure(state="normal")
        self.next_btn.configure(state="normal")
        self.counter_label.configure(text=f"Joke {new_index+1} / {self.total}")

    def _type_setup(self, text):
        self.setup_label.configure(text="")
        self._s_text = text
        self._s_idx = 0
        self._type_setup_step()

    def _type_setup_step(self):
        if self._s_idx <= len(self._s_text):
            self.setup_label.configure(text=self._s_text[:self._s_idx])
            self._s_idx += 1
            pause = 10 if self._s_idx < len(self._s_text) and self._s_text[self._s_idx-1] in ".,!?" else 18
            self.after(pause, self._type_setup_step)

    def show_punchline(self):
        if self.revealing:
            return
        self.revealing = True
        self.show_btn.configure(state="disabled")
        self.after(450, self._type_punchline)

    def _type_punchline(self):
        self._p_text = self.current_punch
        self._p_idx = 0
        self._type_punch_step()

    def _type_punch_step(self):
        if self._p_idx <= len(self._p_text):
            self.punch_label.configure(text=self._p_text[:self._p_idx])
            self._p_idx += 1
            self.after(30, self._type_punch_step)
        else:
            self.revealing = False

# ----------------------------
# Run
# ----------------------------
if __name__ == "__main__":
    app = UltraModernJokeApp()
    app.mainloop()