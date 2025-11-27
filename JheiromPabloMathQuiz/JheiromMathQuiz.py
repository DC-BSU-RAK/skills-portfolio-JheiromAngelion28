import tkinter as tk
from tkinter import messagebox
import random
from tkvideo import tkvideo
from PIL import Image, ImageTk
import os

class MathsQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Maths Quiz")
        self.root.geometry("600x450")
        self.root.resizable(False, False)

       
        try:
            src_jpg = "JheiromPabloMathQuiz/Jheirom’s Math quiz-min.png"
            icon_png = "JheiromPabloMathQuiz/Jheirom’s Math quiz-min.png"
            if os.path.exists(icon_png):
                icon = ImageTk.PhotoImage(file=icon_png)
            elif os.path.exists(src_jpg):
                # convert and save as PNG to prevent any format issues
                img = Image.open(src_jpg)
                img.save(icon_png, format="PNG")
                icon = ImageTk.PhotoImage(img)
            else:
                # fallback: try to use a bundled png name (if user supplied one)
                if os.path.exists("math_quiz_icon.png"):
                    icon = ImageTk.PhotoImage(file="math_quiz_icon.png")
                else:
                    icon = None

            if icon:
                self.root.iconphoto(False, icon)
                self.app_icon = icon  # keep a reference
        except Exception as e:
            # Non-fatal: icon loading shouldn't stop the app
            print("Icon load failed:", e)

        # Track active buttons
        self.selected_difficulty_button = None
        self.selected_operation_button = None

        # Video Background (JheiromMP4 not GIF) 
        # Keep the video in the background; if file missing, app still works.
        self.video_label = tk.Label(self.root)
        self.video_label.pack(fill="both", expand=True)
        try:
            video_path = "JheiromPabloMathQuiz/JheiromMathGIF.mp4"
            if os.path.exists(video_path):
                self.video_player = tkvideo(video_path, self.video_label, loop=1, size=(600, 450))
                self.video_player.play()
            else:
                # If video missing, just fill with background color
                self.video_label.configure(bg="#2b2b2b")
        except Exception as e:
            print("Video background error:", e)
            self.video_label.configure(bg="#2b2b2b")

        # Overlay Frame 
        self.main_frame = tk.Frame(self.root, bg="#000000", bd=0, highlightthickness=0)
        # place centered and a little smaller so the video shows around edges
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Quiz Variables 
        self.difficulty = None
        self.operation_mode = "mixed"
        self.score = 0
        self.current_question = 0
        self.total_questions = 10
        self.first_attempt = True
        self.num1 = self.num2 = self.correct_answer = None
        self.current_operation = None

        # Timer Variables 
        self.timer_length = 15  # seconds per question
        self.timer_running = False
        self.time_left = self.timer_length
        self.timer_canvas = None
        self.timer_bar = None
        self.timer_after_id = None

        # To keep track of popups (so we can explicitly close them)
        self.open_popups = []

        # Start Menu
        self.displayMenu()

    # UI Helpers 
    def clearFrame(self):
        # Destroy any widget children of main_frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def customMessage(self, title, text, color="#28A745", auto_close=None):
        """Create a custom Toplevel popup and keep track of it.
           auto_close: seconds after which popup should auto-close (optional)
        """
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("320x160")
        popup.configure(bg="#111111")
        popup.grab_set()
        popup.transient(self.root)

        # store popup to be able to close it programmatically
        self.open_popups.append(popup)

        tk.Label(popup, text=title, font=("Arial", 16, "bold"), fg=color, bg="#111111").pack(pady=10)
        tk.Label(popup, text=text, font=("Arial", 12), fg="white", bg="#111111", wraplength=280).pack(pady=10)

        btn = tk.Button(popup, text="OK", command=lambda: self._close_popup(popup),
                        bg=color, fg="white", width=10, font=("Arial", 11, "bold"), bd=0, cursor="hand2")
        btn.pack(pady=10)

        if auto_close:
            # auto-close after N seconds
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
        # Close all Toplevel windows the app created
        for popup in list(self.open_popups):
            try:
                popup.destroy()
            except Exception:
                pass
        self.open_popups.clear()

        # Also close any other Toplevel children (defensive)
        for child in self.root.winfo_children():
            if isinstance(child, tk.Toplevel):
                try:
                    child.destroy()
                except Exception:
                    pass

    # Main Menu

    def displayMenu(self):
        self.clearFrame()
        self._cancel_timer()  # ensure no timer is running when on menu

        tk.Label(self.main_frame, text="🧮 MATHS QUIZ 🧠", font=("Arial", 22, "bold"),
                 fg="white", bg="#000000").pack(pady=15)

        tk.Label(self.main_frame, text="Select Difficulty", font=("Arial", 13, "italic"),
                 fg="#f0f0f0", bg="#000000").pack(pady=5)

        button_style = {
            "font": ("Arial", 12, "bold"),
            "width": 20,
            "bg": "#3A91D8",
            "fg": "white",
            "activebackground": "#0663AA",
            "cursor": "hand2",
            "bd": 0
        }

        # Difficulty Buttons
        difficulties = [
            ("Easy (0–9)", "easy"),
            ("Moderate (10–99)", "moderate"),
            ("Advanced (1000–9999)", "advanced")
        ]
        self.difficulty_buttons = []
        for text, level in difficulties:
            btn = tk.Button(self.main_frame, text=text,
                            command=lambda lvl=level, b=text: self.setDifficulty(lvl, b),
                            **button_style)
            btn.pack(pady=5)
            self.difficulty_buttons.append(btn)

        tk.Label(self.main_frame, text="Choose Operation Mode", font=("Arial", 13, "italic"),
                 fg="#f0f0f0", bg="#0A0A0A").pack(pady=10)

        # Operation Buttons 
        operations = [
            ("Addition (+)", "+"),
            ("Subtraction (−)", "-"),
            ("Multiplication (×)", "×"),
            ("Mixed (All)", "mixed")
        ]
        self.operation_buttons = []
        for text, op in operations:
            btn = tk.Button(self.main_frame, text=text,
                            command=lambda mode=op, b=text: self.setOperationMode(mode, b),
                            **button_style)
            btn.pack(pady=5)
            self.operation_buttons.append(btn)

    def setDifficulty(self, level, button_text):
        self.difficulty = level

        for btn in self.difficulty_buttons:
            btn.config(bg="#0078D7")
            if btn.cget("text") == button_text:
                btn.config(bg="#28A745")
                self.selected_difficulty_button = btn

    def setOperationMode(self, mode, button_text):
        if not self.difficulty:
            self.customMessage("⚠️ Choose Difficulty", "Please select a difficulty level first.", "#FFA500")
            return

        self.operation_mode = mode

        for btn in self.operation_buttons:
            btn.config(bg="#0078D7")
            if btn.cget("text") == button_text:
                btn.config(bg="#28A745")
                self.selected_operation_button = btn

        # Reset state for a fresh quiz
        self.score = 0
        self.current_question = 0
        self.startQuiz()

    #  Question Logic 

    def randomInt(self):
        if self.difficulty == "easy":
            return random.randint(0, 9)
        elif self.difficulty == "moderate":
            return random.randint(10, 99)
        else:
            return random.randint(1000, 9999)

    def decideOperation(self):
        if self.operation_mode == "mixed":
            return random.choice(['+', '-', '×'])
        else:
            return self.operation_mode

    def generateQuestion(self):
        self.num1 = self.randomInt()
        self.num2 = self.randomInt()
        self.current_operation = self.decideOperation()

        # Ensure subtraction non-negative
        if self.current_operation == '-' and self.num1 < self.num2:
            self.num1, self.num2 = self.num2, self.num1

        if self.current_operation == '+':
            self.correct_answer = self.num1 + self.num2
        elif self.current_operation == '-':
            self.correct_answer = self.num1 - self.num2
        else:
            self.correct_answer = self.num1 * self.num2

        self.first_attempt = True

    #  Display 

    def startQuiz(self):
        self.generateQuestion()
        self.displayProblem()

    def displayProblem(self):
        self.clearFrame()
        # Cancel any previous timers and popups (ensures clean slate)
        self._cancel_timer()
        self._close_all_popups()

        # Info labels
        tk.Label(self.main_frame, text=f"Question {self.current_question + 1} of {self.total_questions}",
                 font=("Arial", 13, "bold"), fg="white", bg="#000000").pack(pady=5)
        tk.Label(self.main_frame, text=f"Score: {self.score}",
                 font=("Arial", 13), fg="#00FFAA", bg="#000000").pack(pady=5)

        tk.Label(self.main_frame, text=f"{self.num1} {self.current_operation} {self.num2} = ?",
                 font=("Arial", 22, "bold"), fg="#FFD700", bg="#000000").pack(pady=20)

        self.answer_entry = tk.Entry(
            self.main_frame, font=("Arial", 16), width=10, justify="center",
            bg="#111111", fg="#00BFFF", insertbackground="white", relief="flat", bd=5
        )
        self.answer_entry.pack(pady=10)
        self.answer_entry.focus()
        self.answer_entry.bind('<Return>', lambda e: self.checkAnswer())

        self.submit_btn = tk.Button(self.main_frame, text="Submit Answer", command=self.checkAnswer,
                  bg="#28A745", fg="white", activebackground="#218838",
                  font=("Arial", 13, "bold"), width=15, bd=0, cursor="hand2")
        self.submit_btn.pack(pady=10)

        # small hint / instructions
        tk.Label(self.main_frame, text="Press Enter or click Submit. You get more points on first try.",
                 font=("Arial", 9), fg="#CCCCCC", bg="#000000").pack(pady=5)

        self.startTimer()

    # Timer

    def startTimer(self):
        # Ensure no parallel timers
        self._cancel_timer()

        self.timer_canvas = tk.Canvas(self.main_frame, width=400, height=18, bg="#333333", highlightthickness=0)
        self.timer_canvas.pack(pady=10)
        self.timer_bar = self.timer_canvas.create_rectangle(0, 0, 400, 18, fill="#00BFFF", width=0)
        self.time_left = self.timer_length
        self.timer_running = True
        self.updateTimerSmooth()

    def updateTimerSmooth(self):
        if not self.timer_running:
            return

        if not self.timer_canvas:
            return

        bar_width = int(400 * (self.time_left / self.timer_length))

        # Blue → Dark Blue → Purple (interpolated)
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
            # If user fails to answer, show result and proceed
            self.customMessage("⏰ Time’s Up!", f"Out of time! The answer was {self.correct_answer}.", "#8A2BE2", auto_close=2)
            # ensure UI is in known state
            try:
                self.submit_btn.config(state="disabled")
            except Exception:
                pass
            # move to next question after short delay
            self.root.after(2000, self.nextQuestion)
        else:
            self.time_left -= 0.05
            # store after id so we can cancel it later
            self.timer_after_id = self.root.after(50, self.updateTimerSmooth)

    def _cancel_timer(self):
        # Cancel scheduled after() callback if exists
        if self.timer_after_id is not None:
            try:
                self.root.after_cancel(self.timer_after_id)
            except Exception:
                pass
            self.timer_after_id = None
        self.timer_running = False

    # Answer Check

    def checkAnswer(self):
        # Prevent double submission
        self._cancel_timer()
        # disable submit to avoid multiple clicks
        try:
            self.submit_btn.config(state="disabled")
        except Exception:
            pass

        val = self.answer_entry.get().strip()
        try:
            user_answer = int(val)
        except ValueError:
            self.customMessage("⚠️ Invalid Input", "Please enter a number.", "#FFA500")
            # re-enable submit and timer for retry
            try:
                self.submit_btn.config(state="normal")
            except Exception:
                pass
            self.timer_running = True
            self.updateTimerSmooth()
            return

        if user_answer == self.correct_answer:
            self.isCorrect(True)
        else:
            self.isCorrect(False)

    def isCorrect(self, correct):
        if correct:
            if self.first_attempt:
                self.score += 10
                self.customMessage("✅ Correct!", "Well done! +10 points", "#00FF00", auto_close=1.5)
            else:
                self.score += 5
                self.customMessage("✅ Correct!", "Good job! +5 points", "#00FFAA", auto_close=1.5)
            # after a short pause move on
            self.root.after(800, self.nextQuestion)
        else:
            if self.first_attempt:
                self.first_attempt = False
                self.customMessage("❌ Incorrect", "Try again!", "#FF4500", auto_close=1.5)
                # clear entry and re-enable submit and timer for second attempt
                try:
                    self.answer_entry.delete(0, tk.END)
                    self.answer_entry.focus()
                    self.submit_btn.config(state="normal")
                except Exception:
                    pass
                # restart timer for remaining time
                self.timer_running = True
                self.updateTimerSmooth()
            else:
                # second attempt failed
                self.customMessage("❌ Incorrect", f"The answer was {self.correct_answer}.", "#FF0000", auto_close=2)
                self.root.after(1200, self.nextQuestion)

    # Results 

    def nextQuestion(self):
        # Close all popups for clean transition
        self._close_all_popups()

        # increment and either continue or finish
        self.current_question += 1
        # Make sure timers are stopped before proceeding
        self._cancel_timer()

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
        # Reset quiz variables and go to menu
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

# to Run App 
if __name__ == "__main__":
    root = tk.Tk()
    app = MathsQuiz(root)
    root.mainloop()
