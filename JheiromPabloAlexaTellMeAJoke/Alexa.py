import os
import random
import customtkinter as ctk
import tkinter as tk
from tkvideo import tkvideo
from PIL import Image, ImageTk, ImageDraw, ImageFont

# ---------------------------------------
# Window Configuration
# ---------------------------------------
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

JOKES_PATH = os.path.join(BASE_DIR, "randomJokes.txt")
VIDEO_PATH = os.path.join(BASE_DIR, "Jheirom.mp4")


# ---------------------------------------
# Improved GIF Loader (Rectangular + Text)
# ---------------------------------------
class AnimatedGIF:
    def __init__(self, path, size=(250, 100)):
        self.frames = []
        self.index = 0

        gif = Image.open(path)
        self.is_gif = getattr(gif, "is_animated", False)

        try:
            while True:
                frame = gif.copy().convert("RGBA")

                # Resize frame to rectangle (crop to fit)
                frame = self.crop_to_fit(frame, size)

                # Convert to CTkImage for better HiDPI support
                ctk_image = ctk.CTkImage(light_image=frame, dark_image=frame, size=size)
                self.frames.append(ctk_image)

                gif.seek(len(self.frames))

        except EOFError:
            pass

        self.total_frames = len(self.frames)

    def crop_to_fit(self, image, target_size):
        """Crops image to fit target size while maintaining aspect ratio."""
        target_width, target_height = target_size
        img_width, img_height = image.size
        
        # Calculate aspect ratios
        target_ratio = target_width / target_height
        img_ratio = img_width / img_height
        
        if img_ratio > target_ratio:
            # Image is wider, crop width
            new_width = int(img_height * target_ratio)
            left = (img_width - new_width) // 2
            image = image.crop((left, 0, left + new_width, img_height))
        else:
            # Image is taller, crop height
            new_height = int(img_width / target_ratio)
            top = (img_height - new_height) // 2
            image = image.crop((0, top, img_width, top + new_height))
        
        # Resize to target size
        return image.resize(target_size, Image.LANCZOS)

    def next(self):
        frame = self.frames[self.index]
        self.index = (self.index + 1) % self.total_frames
        return frame


# ---------------------------------------
# Joke Loader
# ---------------------------------------
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
    except:
        jokes = [
            ("Why don't scientists trust atoms?", "Because they make up everything."),
            ("What do you call fake spaghetti?", "An impasta."),
            ("Why did the scarecrow win an award?", "Because he was outstanding in his field."),
            ("What happens if you boil a clown?", "You get a laughing stock."),
            ("Why did the chicken cross the road?", "To get to the other side.")
        ]

    return jokes


# ---------------------------------------
# Main App
# ---------------------------------------
class AlexaJokeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Alexa Joke App")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")

        # Load jokes
        self.jokes = load_jokes()
        self.current_joke = None

        # Load GIF buttons
        self.btn_tell = AnimatedGIF(os.path.join(BASE_DIR, "Jokebtn.gif"))
        self.btn_punch = AnimatedGIF(os.path.join(BASE_DIR, "Punchlinebtn.gif"))
        self.btn_next = AnimatedGIF(os.path.join(BASE_DIR, "Nextjokebtn.gif"))
        self.btn_quit = AnimatedGIF(os.path.join(BASE_DIR, "Quitbtn.gif"), size=(150, 60))

        # Build UI
        self._build_ui()

        # Video background
        self._load_video()

        # Animate GIF buttons
        self.animate_buttons()

    # ---------------------------------------
    # UI Layout
    # ---------------------------------------
    def _build_ui(self):
        # Title label
        self.title_label = ctk.CTkLabel(
            self,
            text="Alexa's Joke Box",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="#FFD700",
        )
        self.title_label.place(relx=0.5, y=40, anchor="center")
        
        # Joke setup text (question/setup)
        self.joke_text_label = ctk.CTkLabel(
            self,
            text="Press a button to hear a joke!",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#FFFFFF",
            wraplength=700,
            fg_color="#1a1a2e",
            corner_radius=15,
            padx=25,
            pady=18
        )
        self.joke_text_label.place(relx=0.5, y=200, anchor="center")
        
        # Punchline text (separate)
        self.punchline_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#90EE90",
            wraplength=700,
            fg_color="#2d2d44",
            corner_radius=15,
            padx=25,
            pady=18
        )
        self.punchline_label.place(relx=0.5, y=290, anchor="center")
        self.punchline_label.place_forget()  # Hide initially

        # Calculate even spacing for 3 buttons
        button_width = 250
        total_width = WINDOW_WIDTH
        
        # Main buttons row
        main_spacing = (total_width - (3 * button_width)) / 4
        button_y = 400

        # MAIN BUTTONS with even spacing
        self.show_btn = ctk.CTkButton(self, fg_color="transparent",
                                      text="", image=self.btn_punch.next(),
                                      width=250, height=100,
                                      command=self.show_punchline,
                                      state="disabled",
                                      hover=False)
        self.show_btn.place(x=main_spacing, y=button_y)

        self.tell_btn = ctk.CTkButton(self, fg_color="transparent",
                                      text="", image=self.btn_tell.next(),
                                      width=250, height=100,
                                      command=self.tell_joke,
                                      hover=False)
        self.tell_btn.place(x=main_spacing + button_width + main_spacing, y=button_y)

        self.next_btn = ctk.CTkButton(self, fg_color="transparent",
                                      text="", image=self.btn_next.next(),
                                      width=250, height=100,
                                      command=self.next_joke,
                                      state="disabled",
                                      hover=False)
        self.next_btn.place(x=main_spacing + (button_width + main_spacing) * 2, y=button_y)

        # Quit button - smaller, positioned to the right above next joke button
        self.quit_btn = ctk.CTkButton(self, fg_color="transparent",
                                      text="", image=self.btn_quit.next(),
                                      width=150, height=60,
                                      command=self.quit_app,
                                      hover=False)
        self.quit_btn.place(x=main_spacing + (button_width + main_spacing) * 2 + 50, y=520)

    # ---------------------------------------
    # Video Background
    # ---------------------------------------
    def _load_video(self):
        try:
            if not os.path.exists(VIDEO_PATH):
                return

            self.video_label = tk.Label(self)
            self.video_label.place(x=0, y=0, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
            self.video_label.lower()

            self.video_player = tkvideo(
                VIDEO_PATH,
                self.video_label,
                loop=1,
                size=(WINDOW_WIDTH, WINDOW_HEIGHT)
            )
            self.video_player.play()

        except Exception as e:
            print("Video Error:", e)

    # ---------------------------------------
    # Animate Buttons
    # ---------------------------------------
    def animate_buttons(self):
        self.tell_btn.configure(image=self.btn_tell.next())
        self.show_btn.configure(image=self.btn_punch.next())
        self.next_btn.configure(image=self.btn_next.next())
        self.quit_btn.configure(image=self.btn_quit.next())
        self.after(80, self.animate_buttons)

    # ---------------------------------------
    # Jokes
    # ---------------------------------------
    def tell_joke(self):
        self.current_joke = random.choice(self.jokes)
        setup, _ = self.current_joke
        self.joke_text_label.configure(text=setup)
        self.punchline_label.place_forget()  # Hide punchline
        self.show_btn.configure(state="normal")
        self.next_btn.configure(state="normal")

    def show_punchline(self):
        setup, punchline = self.current_joke
        self.punchline_label.configure(text=punchline)
        self.punchline_label.place(relx=0.5, y=360, anchor="center")  # Show punchline
        self.show_btn.configure(state="disabled")

    def next_joke(self):
        self.tell_joke()

    def quit_app(self):
        self.destroy()


# ---------------------------------------
# Run App
# ---------------------------------------
if __name__ == "__main__":
    app = AlexaJokeApp()
    app.mainloop()