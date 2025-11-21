

import os
import random
import customtkinter as ctk
from PIL import Image, ImageTk  # kept in case you want to add icons later

# ----------------------------
# Configuration
# ----------------------------
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 560
JOKES_PATH = os.path.join(os.path.dirname(__file__), 'randomJokes.txt')

# ----------------------------
# Load jokes
# ----------------------------
def load_jokes(path=JOKES_PATH):
    jokes = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if '?' in line:
                    setup, punch = line.split('?', 1)
                    jokes.append((setup.strip() + '?', punch.strip()))
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
# Joke App Class
# ----------------------------
class ImprovedJokeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Alexa Joke Teller — Modern UI")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(700, 420)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # STATE
        self.jokes = load_jokes()
        self.total = len(self.jokes)
        self.current_index = None
        self.revealing = False
        self.current_setup = ""
        self.current_punchline = ""

        # UI CREATION
        self._create_background()
        self._create_card()
        self._create_controls()
        self._start_neon_animation()
        self._card_float_animation()
        self._show_welcome()

    # ----------------------------
    # Background
    # ----------------------------
    def _create_background(self):
        # pass width/height to constructor (required by customtkinter)
        self.bg_top = ctk.CTkFrame(self, corner_radius=0, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.bg_top.place(x=0, y=0)

        # Decorative stripe (use hex color, not RGB tuple)
        self.left_stripe = ctk.CTkFrame(
            self.bg_top,
            width=160,
            height=WINDOW_HEIGHT - 160,
            corner_radius=20,
            fg_color="#282846"   # replaced tuple with hex
        )
        self.left_stripe.place(x=20, y=80)

    # ----------------------------
    # Main joke card
    # ----------------------------
    def _create_card(self):
        card_w = 740
        card_h = 360
        x = (WINDOW_WIDTH - card_w) // 2
        y = 70

        self.card = ctk.CTkFrame(
            self,
            corner_radius=20,
            border_width=2,
            border_color="#6f6cff",
            width=card_w,
            height=card_h
        )
        self.card.place(x=x, y=y)

        self._card_base_y = y
        self._card_float_offset = 0
        self._card_float_dir = 1

        # Title row
        top = ctk.CTkFrame(self.card, fg_color="transparent")
        top.pack(padx=20, pady=(16, 6), fill="x")

        ctk.CTkLabel(top, text="Alexa Joke Teller", font=ctk.CTkFont(size=20, weight="bold")).pack(side="left")

        # mic button: use transparent fg_color and remove unsupported kwargs
        mic = ctk.CTkButton(top, text="🎙️", width=36, height=36, corner_radius=18, fg_color="transparent", command=self._mic_pressed)
        mic.pack(side="right")

        # Joke display area - use hex color instead of tuple
        self.joke_frame = ctk.CTkFrame(self.card, corner_radius=14, fg_color="#1e1e28")
        self.joke_frame.pack(padx=18, pady=8, expand=True, fill="both")

        self.setup_label = ctk.CTkLabel(self.joke_frame, text="", wraplength=640, justify="center", font=ctk.CTkFont(size=18))
        self.setup_label.pack(pady=(18, 6), padx=18)

        self.punch_label = ctk.CTkLabel(self.joke_frame, text="", wraplength=640, justify="center", font=ctk.CTkFont(size=18, slant="italic"))
        self.punch_label.pack(pady=(6, 12), padx=18)

        # Counter
        bottom = ctk.CTkFrame(self.card, fg_color="transparent")
        bottom.pack(padx=20, pady=(0, 12), fill="x")

        self.counter_label = ctk.CTkLabel(bottom, text="Joke 0 / 0", font=ctk.CTkFont(size=12))
        self.counter_label.pack(side="left")

        self.spinner = ctk.CTkProgressBar(bottom, mode="indeterminate")
        self.spinner.pack(side="right", fill="x", expand=True)
        try:
            self.spinner.stop()
        except Exception:
            pass

    # ----------------------------
    # Controls
    # ----------------------------
    def _create_controls(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        # place without width/height (frame can be sized by contents)
        frame.place(relx=0.5, rely=0.82, anchor="n")

        self.tell_btn = ctk.CTkButton(frame, text="Alexa Tell Me a Joke", width=220, command=self.tell_joke)
        self.tell_btn.grid(row=0, column=0, padx=12, pady=6)

        self.show_btn = ctk.CTkButton(frame, text="Show Punchline", width=180, command=self.show_punchline, state="disabled")
        self.show_btn.grid(row=0, column=1, padx=12, pady=6)

        self.next_btn = ctk.CTkButton(frame, text="Next Joke", width=130, command=self.tell_joke, state="disabled")
        self.next_btn.grid(row=0, column=2, padx=12, pady=6)

        self.quit_btn = ctk.CTkButton(frame, text="Quit", width=90, command=self.destroy)
        self.quit_btn.grid(row=0, column=3, padx=12, pady=6)

    # ----------------------------
    # Mic flash
    # ----------------------------
    def _mic_pressed(self):
        original = self.card.cget("border_color")
        # visual flash
        self.card.configure(border_color="#ffd86b")
        self.after(220, lambda: self.card.configure(border_color=original))
        self.after(330, self.tell_joke)

    # ----------------------------
    # Neon animation
    # ----------------------------
    def _start_neon_animation(self):
        self._neon_phase = 0
        self._neon_dir = 1
        self._neon_step()

    def _neon_step(self):
        phase = (self._neon_phase % 100) / 100.0
        color_a = (111, 111, 255)
        color_b = (96, 159, 255)
        r = int(color_a[0] + (color_b[0] - color_a[0]) * phase)
        g = int(color_a[1] + (color_b[1] - color_a[1]) * phase)
        bl = int(color_a[2] + (color_b[2] - color_a[2]) * phase)
        try:
            self.card.configure(border_color=f"#{r:02x}{g:02x}{bl:02x}")
        except Exception:
            pass

        self._neon_phase += self._neon_dir * 2
        if self._neon_phase >= 100 or self._neon_phase <= 0:
            self._neon_dir *= -1

        self.after(60, self._neon_step)

    # ----------------------------
    # Floating card animation
    # ----------------------------
    def _card_float_animation(self):
        self._card_float_offset += self._card_float_dir
        if abs(self._card_float_offset) > 8:
            self._card_float_dir *= -1
        new_y = self._card_base_y + self._card_float_offset
        try:
            self.card.place_configure(y=new_y)
        except Exception:
            pass
        self.after(120, self._card_float_animation)

    # ----------------------------
    # Joke Logic
    # ----------------------------
    def _show_welcome(self):
        self.setup_label.configure(text="Press 'Alexa Tell Me a Joke' or tap the mic 🎙️")
        self.punch_label.configure(text="")
        self.counter_label.configure(text=f"Joke 0 / {self.total}")

    def tell_joke(self):
        if not self.jokes:
            return

        new_index = random.randrange(len(self.jokes))
        if self.current_index == new_index and len(self.jokes) > 1:
            new_index = (new_index + 1) % len(self.jokes)

        self.current_index = new_index
        self.current_setup, self.current_punchline = self.jokes[new_index]

        self._type_setup(self.current_setup)
        self.punch_label.configure(text="")

        self.show_btn.configure(state="normal")
        self.next_btn.configure(state="normal")

        self.counter_label.configure(text=f"Joke {new_index+1} / {self.total}")

    # ----------------------------
    # Typing animations
    # ----------------------------
    def _type_setup(self, text):
        self.setup_label.configure(text="")
        self._s_idx = 0
        self._s_text = text
        self._type_setup_step()

    def _type_setup_step(self):
        if self._s_idx <= len(self._s_text):
            self.setup_label.configure(text=self._s_text[:self._s_idx])
            self._s_idx += 1
            self.after(12, self._type_setup_step)

    def show_punchline(self):
        if self.revealing:
            return
        self.revealing = True
        self.show_btn.configure(state="disabled")

        try:
            self.spinner.start()
        except Exception:
            pass

        self.after(600, self._type_punchline)

    def _type_punchline(self):
        try:
            self.spinner.stop()
        except Exception:
            pass

        self._p_idx = 0
        self._p_text = self.current_punchline
        self._type_punch_step()

    def _type_punch_step(self):
        if self._p_idx <= len(self._p_text):
            self.punch_label.configure(text=self._p_text[:self._p_idx])
            self._p_idx += 1
            self.after(28, self._type_punch_step)
        else:
            self.revealing = False


# ----------------------------
# Run App
# ----------------------------
if __name__ == "__main__":
    app = ImprovedJokeApp()
    app.mainloop()
