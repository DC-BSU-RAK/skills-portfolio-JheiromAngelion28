import tkinter as tk
from tkinter import messagebox
import random
from tkvideo import tkvideo
from PIL import Image, ImageTk, ImageSequence
import os

class MathsQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Maths Quiz")
        self.root.geometry("600x450")
        self.root.resizable(False, False)

        # --- App Icon ---
        self.setup_icon()

        # Track active buttons
        self.selected_difficulty_button = None
        self.selected_operation_button = None

        # --- Video Background ---
        self.setup_video_background()

        # --- Overlay Frame ---
        self.main_frame = tk.Frame(self.root, bg="#000000", bd=0, highlightthickness=0)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # --- Quiz Variables ---
        self.difficulty = None
        self.operation_mode = "mixed"
        self.score = 0
        self.current_question = 0
        self.total_questions = 10
        self.first_attempt = True
        self.num1 = self.num2 = self.correct_answer = None
        self.current_operation = None

        # --- Timer Variables ---
        self.timer_length = 15
        self.timer_running = False
        self.time_left = self.timer_length
        self.timer_canvas = None
        self.timer_bar = None
        self.timer_after_id = None

        # Track popups
        self.open_popups = []

        # --- Start Menu ---
        self.displayMenu()

    def setup_icon(self):
        """Setup application icon with multiple fallback options"""
        icon_paths = [
            "JheiromPabloMathQuiz/Jheirom's Math quiz.png",
            "JheiromPabloMathQuiz/Jheirom's Math quiz-min.png",
            "/mnt/data/Jheirom's Math quiz.jpg",
            "icon.png",
            "math_quiz_icon.png"
        ]
        
        icon = None
        for path in icon_paths:
            try:
                if os.path.exists(path):
                    if path.endswith('.jpg'):
                        img = Image.open(path)
                        icon_path_png = "converted_icon.png"
                        img.save(icon_path_png, format="PNG")
                        icon = ImageTk.PhotoImage(file=icon_path_png)
                    else:
                        icon = ImageTk.PhotoImage(file=path)
                    break
            except Exception as e:
                print(f"Icon load failed for {path}: {e}")
                continue
        
        if icon:
            self.root.iconphoto(False, icon)
            self.app_icon = icon
        else:
            print("No icon found, using default")

    def setup_video_background(self):
        """Setup video background with fallback to GIF or solid color"""
        self.video_label = tk.Label(self.root)
        self.video_label.pack(fill="both", expand=True)
        
        video_paths = [
            "JheiromPabloMathQuiz/JheiromMathGIF.mp4",
            "JheiromMathGIF.mp4",
            "background.mp4",
            "JheiromPabloMathQuiz/JheiromMathGIF.gif",
            "background.gif"
        ]
        
        video_loaded = False
        
        # Try MP4 files first
        for video_path in video_paths[:3]:  # First 3 are MP4 paths
            try:
                if os.path.exists(video_path):
                    self.video_player = tkvideo(video_path, self.video_label, loop=1, size=(600, 450))
                    self.video_player.play()
                    video_loaded = True
                    print(f"Video background loaded: {video_path}")
                    break
            except Exception as e:
                print(f"Video background error for {video_path}: {e}")
                continue
        
        # If MP4 failed, try GIF files
        if not video_loaded:
            for gif_path in video_paths[3:]:  # Last 2 are GIF paths
                try:
                    if os.path.exists(gif_path):
                        self.setup_gif_background(gif_path)
                        video_loaded = True
                        break
                except Exception as e:
                    print(f"GIF background error for {gif_path}: {e}")
                    continue
        
        # Final fallback to solid color
        if not video_loaded:
            self.video_label.configure(bg="#2b2b2b")
            print("Using solid color background")

    def setup_gif_background(self, gif_path):
        """Setup animated GIF as background"""
        try:
            gif = Image.open(gif_path)
            frames = []
            for frame in ImageSequence.Iterator(gif):
                frame = frame.copy()
                frame = frame.resize((600, 450), Image.Resampling.LANCZOS)
                frames.append(ImageTk.PhotoImage(frame))
            
            self.bg_frames = frames
            self.bg_frame_index = 0
            self.animate_background()
        except Exception as e:
            print(f"GIF background setup failed: {e}")
            self.video_label.configure(bg="#2b2b2b")

    def animate_background(self):
        """Animate the GIF background"""
        if hasattr(self, 'bg_frames'):
            self.video_label.configure(image=self.bg_frames[self.bg_frame_index])
            self.bg_frame_index = (self.bg_frame_index + 1) % len(self.bg_frames)
            self.root.after(100, self.animate_background)

    # ================== UI Helpers ==================
    def clearFrame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def customMessage(self, title, text, color="#28A745", auto_close=None):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("320x160")
        popup.configure(bg="#111111")
        popup.grab_set()
        popup.transient(self.root)
        self.open_popups.append(popup)

        tk.Label(popup, text=title, font=("Arial", 16, "bold"), fg=color, bg="#111111").pack(pady=10)
        tk.Label(popup, text=text, font=("Arial", 12), fg="white", bg="#111111", wraplength=280).pack(pady=10)

        btn = tk.Button(popup, text="OK", command=lambda: self._close_popup(popup),
                        bg=color, fg="white", width=10, font=("Arial", 11, "bold"), bd=0, cursor="hand2")
        btn.pack(pady=10)

        if auto_close:
            popup.after(int(auto_close * 1000), lambda: self._close_popup(popup))

        return popup

    def _close_popup(self, popup):
        try:
            if popup in self.open_popups:
                self.open_popups.remove(popup)
            popup.destroy()
        except Exception:
            pass

    def _close_all_popups(self):
        for popup in list(self.open_popups):
            try:
                popup.destroy()
            except Exception:
                pass
        self.open_popups.clear()
        for child in self.root.winfo_children():
            if isinstance(child, tk.Toplevel):
                try:
                    child.destroy()
                except Exception:
                    pass

    # ================== Main Menu with GIF Buttons ==================
    def displayMenu(self):
        self.clearFrame()
        self._cancel_timer()

        tk.Label(self.main_frame, text="🧮 MATHS QUIZ 🧠", font=("Arial", 22, "bold"),
                 fg="white", bg="#000000").pack(pady=15)
        tk.Label(self.main_frame, text="Select Difficulty", font=("Arial", 13, "italic"),
                 fg="#f0f0f0", bg="#000000").pack(pady=5)

        # --- Difficulty buttons with GIF fallback ---
        self.setup_difficulty_buttons()
        
        tk.Label(self.main_frame, text="Choose Operation Mode", font=("Arial", 13, "italic"),
                 fg="#f0f0f0", bg="#000000").pack(pady=10)

        # --- Operation buttons with GIF fallback ---
        self.setup_operation_buttons()

    def setup_difficulty_buttons(self):
        """Setup difficulty selection buttons with GIF support"""
        difficulties = [
            ("Easy (0–9)", "easy", "Easy.gif"),
            ("Moderate (10–99)", "moderate", "Moderate.gif"),
            ("Advanced (1000–9999)", "advanced", "Advanced.gif")
        ]
        self.difficulty_buttons = []
        self.difficulty_gifs = {}

        for text, level, gif_path in difficulties:
            if self.load_gif_button(text, level, gif_path, "difficulty"):
                continue  # GIF loaded successfully
            
            # Fallback to regular button
            btn = tk.Button(self.main_frame, text=text,
                            command=lambda lvl=level, b=text: self.setDifficulty(lvl, b),
                            font=("Arial", 12, "bold"), width=20, bg="#0078D7", fg="white",
                            cursor="hand2", bd=0)
            btn.pack(pady=5)
            self.difficulty_buttons.append(btn)

    def setup_operation_buttons(self):
        """Setup operation selection buttons with GIF support"""
        operations = [
            ("Addition (+)", "+", "Addition.gif"),
            ("Subtraction (−)", "-", "Subtraction.gif"),
            ("Multiplication (×)", "×", "Multiplication.gif"),
            ("Mixed (All)", "mixed", "Mixed.gif")
        ]
        self.operation_buttons = []
        self.operation_gifs = {}

        for text, op, gif_path in operations:
            if self.load_gif_button(text, op, gif_path, "operation"):
                continue  # GIF loaded successfully
            
            # Fallback to regular button
            btn = tk.Button(self.main_frame, text=text,
                            command=lambda mode=op, b=text: self.setOperationMode(mode, b),
                            font=("Arial", 12, "bold"), width=20, bg="#0078D7", fg="white",
                            cursor="hand2", bd=0)
            btn.pack(pady=5)
            self.operation_buttons.append(btn)

    def load_gif_button(self, text, value, gif_path, button_type):
        """Load GIF button if available, return True if successful"""
        expanded_paths = [
            gif_path,
            f"JheiromPabloMathQuiz/{gif_path}",
            f"assets/{gif_path}",
            f"images/{gif_path}"
        ]
        
        actual_path = None
        for path in expanded_paths:
            if os.path.exists(path):
                actual_path = path
                break
        
        if not actual_path:
            print(f"GIF not found: {gif_path}")
            return False

        try:
            gif = Image.open(actual_path)
            frames = [ImageTk.PhotoImage(f.copy().convert("RGBA")) for f in ImageSequence.Iterator(gif)]

            lbl = tk.Label(self.main_frame, bg="#000000", cursor="hand2")
            lbl.pack(pady=5)
            
            if button_type == "difficulty":
                self.difficulty_buttons.append(lbl)
                self.difficulty_gifs[text] = frames
            else:
                self.operation_buttons.append(lbl)
                self.operation_gifs[text] = frames

            def animate(label=lbl, frames=frames, index=0):
                if label.winfo_exists():
                    label.config(image=frames[index])
                    label.image = frames[index]
                    self.root.after(100, animate, label, frames, (index + 1) % len(frames))

            animate()
            
            if button_type == "difficulty":
                lbl.bind("<Button-1>", lambda e, lvl=value, txt=text: self._selectDifficultyGIF(lvl, txt))
            else:
                lbl.bind("<Button-1>", lambda e, mode=value, txt=text: self._selectOperationGIF(mode, txt))
            
            return True
            
        except Exception as e:
            print(f"Failed to load GIF {actual_path}: {e}")
            return False

    # ================== GIF Button Highlight Handlers ==================
    def _selectDifficultyGIF(self, level, button_text):
        self.difficulty = level
        for lbl in self.difficulty_buttons:
            lbl.config(bg="#000000")
        for idx, text in enumerate(self.difficulty_gifs.keys()):
            if text == button_text:
                self.difficulty_buttons[idx].config(bg="#28A745")
        print(f"Difficulty set to {level}")

    def _selectOperationGIF(self, mode, button_text):
        if not self.difficulty:
            self.customMessage("⚠️ Choose Difficulty", "Please select a difficulty level first.", "#FFA500")
            return
        self.operation_mode = mode
        for lbl in self.operation_buttons:
            lbl.config(bg="#000000")
        for idx, text in enumerate(self.operation_gifs.keys()):
            if text == button_text:
                self.operation_buttons[idx].config(bg="#28A745")
        print(f"Operation mode set to {mode}")
        self.score = 0
        self.current_question = 0
        self.startQuiz()

    # ================== Button Handlers for Regular Buttons ==================
    def setDifficulty(self, level, button_text):
        self.difficulty = level
        print(f"Difficulty set to {level}")

    def setOperationMode(self, mode, button_text):
        if not self.difficulty:
            self.customMessage("⚠️ Choose Difficulty", "Please select a difficulty level first.", "#FFA500")
            return
        self.operation_mode = mode
        print(f"Operation mode set to {mode}")
        self.score = 0
        self.current_question = 0
        self.startQuiz()

    # ================== Random Question Logic ==================
    def randomInt(self):
        if self.difficulty == "easy": return random.randint(0, 9)
        elif self.difficulty == "moderate": return random.randint(10, 99)
        else: return random.randint(1000, 9999)

    def decideOperation(self):
        return random.choice(['+', '-', '×']) if self.operation_mode == "mixed" else self.operation_mode

    def generateQuestion(self):
        self.num1 = self.randomInt()
        self.num2 = self.randomInt()
        self.current_operation = self.decideOperation()
        if self.current_operation == '-' and self.num1 < self.num2:
            self.num1, self.num2 = self.num2, self.num1
        self.correct_answer = self.num1 + self.num2 if self.current_operation == '+' else \
                              self.num1 - self.num2 if self.current_operation == '-' else \
                              self.num1 * self.num2
        self.first_attempt = True

    # ================== Quiz Display & Timer ==================
    def startQuiz(self):
        self.generateQuestion()
        self.displayProblem()

    def displayProblem(self):
        self.clearFrame()
        self._cancel_timer()
        self._close_all_popups()

        tk.Label(self.main_frame, text=f"Question {self.current_question + 1} of {self.total_questions}",
                 font=("Arial", 13, "bold"), fg="white", bg="#000000").pack(pady=5)
        tk.Label(self.main_frame, text=f"Score: {self.score}",
                 font=("Arial", 13), fg="#00FFAA", bg="#000000").pack(pady=5)
        tk.Label(self.main_frame, text=f"{self.num1} {self.current_operation} {self.num2} = ?",
                 font=("Arial", 22, "bold"), fg="#FFD700", bg="#000000").pack(pady=20)

        self.answer_entry = tk.Entry(self.main_frame, font=("Arial", 16), width=10,
                                     justify="center", bg="#111111", fg="#00BFFF", insertbackground="white",
                                     relief="flat", bd=5)
        self.answer_entry.pack(pady=10)
        self.answer_entry.focus()
        self.answer_entry.bind('<Return>', lambda e: self.checkAnswer())

        self.submit_btn = tk.Button(self.main_frame, text="Submit Answer", command=self.checkAnswer,
                                    bg="#28A745", fg="white", activebackground="#218838",
                                    font=("Arial", 13, "bold"), width=15, bd=0, cursor="hand2")
        self.submit_btn.pack(pady=10)

        tk.Label(self.main_frame, text="Press Enter or click Submit. You get more points on first try.",
                 font=("Arial", 9), fg="#CCCCCC", bg="#000000").pack(pady=5)

        self.startTimer()

    def startTimer(self):
        self._cancel_timer()
        self.timer_canvas = tk.Canvas(self.main_frame, width=400, height=18, bg="#333333", highlightthickness=0)
        self.timer_canvas.pack(pady=10)
        self.timer_bar = self.timer_canvas.create_rectangle(0, 0, 400, 18, fill="#00BFFF", width=0)
        self.time_left = self.timer_length
        self.timer_running = True
        self.updateTimerSmooth()

    def updateTimerSmooth(self):
        if not self.timer_running or not self.timer_canvas: return
        bar_width = int(400 * (self.time_left / self.timer_length))
        t = max(0.0, min(1.0, self.time_left / self.timer_length))
        r = int(0 + (138 - 0) * (1 - t))
        g = int(191 + (43 - 191) * (1 - t))
        b = int(255 + (226 - 255) * (1 - t))
        color = f"#{r:02X}{g:02X}{b:02X}"
        self.timer_canvas.coords(self.timer_bar, 0, 0, bar_width, 18)
        self.timer_canvas.itemconfig(self.timer_bar, fill=color)

        if self.time_left <= 0:
            self.timer_running = False
            self._cancel_timer()
            self.customMessage("⏰ Time's Up!", f"Out of time! The answer was {self.correct_answer}.", "#8A2BE2", auto_close=2)
            try: self.submit_btn.config(state="disabled")
            except Exception: pass
            self.root.after(2000, self.nextQuestion)
        else:
            self.time_left -= 0.05
            self.timer_after_id = self.root.after(50, self.updateTimerSmooth)

    def _cancel_timer(self):
        if self.timer_after_id is not None:
            try: self.root.after_cancel(self.timer_after_id)
            except Exception: pass
            self.timer_after_id = None
        self.timer_running = False

    # ================== Answer Checking ==================
    def checkAnswer(self):
        self._cancel_timer()
        try: self.submit_btn.config(state="disabled")
        except Exception: pass
        val = self.answer_entry.get().strip()
        try:
            user_answer = int(val)
        except ValueError:
            self.customMessage("⚠️ Invalid Input", "Please enter a number.", "#FFA500")
            try: self.submit_btn.config(state="normal")
            except Exception: pass
            self.timer_running = True
            self.updateTimerSmooth()
            return

        if user_answer == self.correct_answer: self.isCorrect(True)
        else: self.isCorrect(False)

    def isCorrect(self, correct):
        if correct:
            points = 10 if self.first_attempt else 5
            self.score += points
            self.customMessage("✅ Correct!", f"Well done! +{points} points", "#00FF00", auto_close=1.5)
            self.root.after(800, self.nextQuestion)
        else:
            if self.first_attempt:
                self.first_attempt = False
                self.customMessage("❌ Incorrect", "Try again!", "#FF4500", auto_close=1.5)
                try: self.answer_entry.delete(0, tk.END); self.answer_entry.focus(); self.submit_btn.config(state="normal")
                except Exception: pass
                self.timer_running = True
                self.updateTimerSmooth()
            else:
                self.customMessage("❌ Incorrect", f"The answer was {self.correct_answer}.", "#FF0000", auto_close=2)
                self.root.after(1200, self.nextQuestion)

    # ================== Quiz Flow ==================
    def nextQuestion(self):
        self._close_all_popups()
        self._cancel_timer()
        self.current_question += 1
        if self.current_question < self.total_questions:
            self.generateQuestion()
            self.displayProblem()
        else:
            self.displayResults()

    def displayResults(self):
        self.clearFrame()
        self._cancel_timer()
        self._close_all_popups()

        grade = self.calculateGrade()
        tk.Label(self.main_frame, text="🏁 QUIZ COMPLETE 🏁", font=("Arial", 20, "bold"),
                 fg="white", bg="#000000").pack(pady=20)
        tk.Label(self.main_frame, text=f"Score: {self.score}/100", font=("Arial", 16),
                 fg="#00FFAA", bg="#000000").pack(pady=5)
        tk.Label(self.main_frame, text=f"Grade: {grade}", font=("Arial", 16, "bold"),
                 fg="#FFD700", bg="#000000").pack(pady=5)
        tk.Button(self.main_frame, text="Play Again", bg="#0078D7", fg="white",
                  activebackground="#005A9E", font=("Arial", 13, "bold"),
                  width=15, bd=0, cursor="hand2", command=self._play_again).pack(pady=10)
        tk.Button(self.main_frame, text="Exit", bg="#DC3545", fg="white",
                  activebackground="#B02A37", font=("Arial", 13, "bold"),
                  width=15, bd=0, cursor="hand2", command=self.root.quit).pack(pady=10)

    def _play_again(self):
        self.score = 0
        self.current_question = 0
        self.difficulty = None
        self.operation_mode = "mixed"
        self._cancel_timer()
        self.displayMenu()

    def calculateGrade(self):
        if self.score >= 90: return "A+"
        elif self.score >= 80: return "A"
        elif self.score >= 70: return "B"
        elif self.score >= 60: return "C"
        elif self.score >= 50: return "D"
        else: return "F"

# ================== Run App ==================
if __name__ == "__main__":
    root = tk.Tk()
    app = MathsQuiz(root)
    root.mainloop()