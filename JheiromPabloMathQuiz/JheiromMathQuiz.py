import tkinter as tk
from tkinter import messagebox
import random
from tkvideo import tkvideo
from PIL import Image, ImageTk

class MathsQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Maths Quiz")
        self.root.geometry("600x450")
        self.root.resizable(False, False)

        # Track active buttons
        self.selected_difficulty_button = None
        self.selected_operation_button = None

        # === Video Background ===
        self.video_label = tk.Label(self.root)
        self.video_label.pack(fill="both", expand=True)
        self.video_player = tkvideo("JheiromPabloMathQuiz/JheiromMathGIF.mp4", self.video_label, loop=1, size=(600, 450))
        self.video_player.play()

        # === Overlay Frame ===
        self.main_frame = tk.Frame(self.root, bg="#000000", bd=0, highlightthickness=0)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # === Quiz Variables ===
        self.difficulty = None
        self.operation_mode = "mixed"
        self.score = 0
        self.current_question = 0
        self.total_questions = 10
        self.first_attempt = True
        self.num1 = self.num2 = self.correct_answer = None
        self.current_operation = None

        # === Timer Variables ===
        self.timer_length = 15  # seconds per question
        self.timer_running = False
        self.time_left = self.timer_length
        self.timer_canvas = None
        self.timer_bar = None

        # === Start Menu ===
        self.displayMenu()

    # ================== UI Helpers ==================

    def clearFrame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def customMessage(self, title, text, color="#28A745"):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("320x160")
        popup.configure(bg="#111111")
        popup.grab_set()

        tk.Label(popup, text=title, font=("Arial", 16, "bold"), fg=color, bg="#111111").pack(pady=10)
        tk.Label(popup, text=text, font=("Arial", 12), fg="white", bg="#111111", wraplength=280).pack(pady=10)
        tk.Button(popup, text="OK", command=popup.destroy, bg=color, fg="white",
                  width=10, font=("Arial", 11, "bold"), bd=0, cursor="hand2").pack(pady=10)

    # ================== Main Menu ==================

    def displayMenu(self):
        self.clearFrame()

        tk.Label(self.main_frame, text="🧮 MATHS QUIZ 🧠", font=("Arial", 22, "bold"),
                 fg="white", bg="#000000").pack(pady=15)

        tk.Label(self.main_frame, text="Select Difficulty", font=("Arial", 13, "italic"),
                 fg="#f0f0f0", bg="#000000").pack(pady=5)

        button_style = {
            "font": ("Arial", 12, "bold"),
            "width": 20,
            "bg": "#0078D7",
            "fg": "white",
            "activebackground": "#005A9E",
            "cursor": "hand2",
            "bd": 0
        }

        # --- Difficulty Buttons ---
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
                 fg="#f0f0f0", bg="#000000").pack(pady=10)

        # --- Operation Buttons ---
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

        self.score = 0
        self.current_question = 0
        self.startQuiz()

    # ================== Question Logic ==================

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

        if self.current_operation == '-' and self.num1 < self.num2:
            self.num1, self.num2 = self.num2, self.num1

        if self.current_operation == '+':
            self.correct_answer = self.num1 + self.num2
        elif self.current_operation == '-':
            self.correct_answer = self.num1 - self.num2
        else:
            self.correct_answer = self.num1 * self.num2

        self.first_attempt = True

    # ================== Quiz Display ==================

    def startQuiz(self):
        self.generateQuestion()
        self.displayProblem()

    def displayProblem(self):
        self.clearFrame()

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

        tk.Button(self.main_frame, text="Submit Answer", command=self.checkAnswer,
                  bg="#28A745", fg="white", activebackground="#218838",
                  font=("Arial", 13, "bold"), width=15, bd=0, cursor="hand2").pack(pady=10)

        self.startTimer()

    # ================== Timer ==================

    def startTimer(self):
        self.timer_canvas = tk.Canvas(self.main_frame, width=400, height=18, bg="#333333", highlightthickness=0)
        self.timer_canvas.pack(pady=10)
        self.timer_bar = self.timer_canvas.create_rectangle(0, 0, 400, 18, fill="#00BFFF", width=0)
        self.time_left = self.timer_length
        self.timer_running = True
        self.updateTimerSmooth()

    def updateTimerSmooth(self):
        if not self.timer_running:
            return

        bar_width = int(400 * (self.time_left / self.timer_length))

        # Blue → Dark Blue → Purple
        t = self.time_left / self.timer_length
        r = int(0 + (138 - 0) * (1 - t))
        g = int(191 + (43 - 191) * (1 - t))
        b = int(255 + (226 - 255) * (1 - t))
        color = f"#{r:02X}{g:02X}{b:02X}"

        self.timer_canvas.coords(self.timer_bar, 0, 0, bar_width, 18)
        self.timer_canvas.itemconfig(self.timer_bar, fill=color)

        if self.time_left <= 0:
            self.timer_running = False
            self.customMessage("⏰ Time’s Up!", f"Out of time! The answer was {self.correct_answer}.", "#8A2BE2")
            self.nextQuestion()
        else:
            self.time_left -= 0.05
            self.root.after(50, self.updateTimerSmooth)

    # ================== Answer Check ==================

    def checkAnswer(self):
        self.timer_running = False
        try:
            user_answer = int(self.answer_entry.get())
        except ValueError:
            self.customMessage("⚠️ Invalid Input", "Please enter a number.", "#FFA500")
            return

        if user_answer == self.correct_answer:
            self.isCorrect(True)
        else:
            self.isCorrect(False)

    def isCorrect(self, correct):
        if correct:
            if self.first_attempt:
                self.score += 10
                self.customMessage("✅ Correct!", "Well done! +10 points", "#00FF00")
            else:
                self.score += 5
                self.customMessage("✅ Correct!", "Good job! +5 points", "#00FFAA")
            self.nextQuestion()
        else:
            if self.first_attempt:
                self.first_attempt = False
                self.customMessage("❌ Incorrect", "Try again!", "#FF4500")
                self.answer_entry.delete(0, tk.END)
                self.answer_entry.focus()
                self.timer_running = True
                self.updateTimerSmooth()
            else:
                self.customMessage("❌ Incorrect", f"The answer was {self.correct_answer}.", "#FF0000")
                self.nextQuestion()

    # ================== Results ==================

    def nextQuestion(self):
        self.current_question += 1
        if self.current_question < self.total_questions:
            self.generateQuestion()
            self.displayProblem()
        else:
            self.displayResults()

    def displayResults(self):
        self.clearFrame()
        grade = self.calculateGrade()

        tk.Label(self.main_frame, text="🏁 QUIZ COMPLETE 🏁", font=("Arial", 20, "bold"),
                 fg="white", bg="#000000").pack(pady=20)
        tk.Label(self.main_frame, text=f"Score: {self.score}/100", font=("Arial", 16),
                 fg="#00FFAA", bg="#000000").pack(pady=5)
        tk.Label(self.main_frame, text=f"Grade: {grade}", font=("Arial", 16, "bold"),
                 fg="#FFD700", bg="#000000").pack(pady=5)

        tk.Button(self.main_frame, text="Play Again", bg="#0078D7", fg="white",
                  activebackground="#005A9E", font=("Arial", 13, "bold"),
                  width=15, bd=0, cursor="hand2", command=self.displayMenu).pack(pady=10)

        tk.Button(self.main_frame, text="Exit", bg="#DC3545", fg="white",
                  activebackground="#B02A37", font=("Arial", 13, "bold"),
                  width=15, bd=0, cursor="hand2", command=self.root.quit).pack(pady=10)

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
