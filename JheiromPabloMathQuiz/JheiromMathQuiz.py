import tkinter as tk
from tkinter import messagebox
import random
from tkvideo import tkvideo  # <-- new import for video playback

class MathsQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Maths Quiz")
        self.root.geometry("600x450")
        self.root.resizable(False, False)
        
        # === Video Background ===
        self.video_label = tk.Label(self.root)
        self.video_label.pack(fill="both", expand=True)
        self.video_player = tkvideo("JheiromPabloMathQuiz/JheiromMathGIF.mp4", self.video_label, loop=1, size=(600, 450))
        self.video_player.play()

        # === Overlay Frame for Quiz ===
        self.main_frame = tk.Frame(self.root, bg="#000000", bd=0, highlightthickness=0)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Quiz variables
        self.difficulty = None
        self.score = 0
        self.current_question = 0
        self.total_questions = 10
        self.first_attempt = True
        self.current_operation = None
        self.num1 = None
        self.num2 = None
        self.correct_answer = None
        
        self.displayMenu()

    def clearFrame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def displayMenu(self):
        self.clearFrame()
        self.main_frame.configure(bg="#000000")
        
        title_label = tk.Label(self.main_frame, text="🧮 MATHS QUIZ 🧠",
                               font=("Arial", 20, "bold"), fg="white", bg="#000000")
        title_label.pack(pady=20)
        
        subtitle = tk.Label(self.main_frame, text="Select Difficulty Level",
                            font=("Arial", 14, "italic"), fg="#f0f0f0", bg="#000000")
        subtitle.pack(pady=5)
        
        button_style = {
            "font": ("Arial", 13, "bold"),
            "width": 20,
            "bg": "#0078D7",
            "fg": "white",
            "activebackground": "#005A9E",
            "cursor": "hand2",
            "bd": 0,
            "relief": "flat"
        }
        
        tk.Button(self.main_frame, text="Easy (0-9)", command=lambda: self.setDifficulty("easy"), **button_style).pack(pady=10)
        tk.Button(self.main_frame, text="Moderate (10-99)", command=lambda: self.setDifficulty("moderate"), **button_style).pack(pady=10)
        tk.Button(self.main_frame, text="Advanced (1000-9999)", command=lambda: self.setDifficulty("advanced"), **button_style).pack(pady=10)
        
        info_label = tk.Label(self.main_frame,
                              text="You will get 10 questions.\n10 points for first try, 5 for second try.",
                              font=("Arial", 10), fg="white", bg="#000000")
        info_label.pack(pady=15)

    def setDifficulty(self, level):
        self.difficulty = level
        self.score = 0
        self.current_question = 0
        self.startQuiz()

    def randomInt(self):
        if self.difficulty == "easy":
            return random.randint(0, 9)
        elif self.difficulty == "moderate":
            return random.randint(10, 99)
        else:
            return random.randint(1000, 9999)

    def decideOperation(self):
        return random.choice(['+', '-'])

    def generateQuestion(self):
        self.num1 = self.randomInt()
        self.num2 = self.randomInt()
        self.current_operation = self.decideOperation()
        if self.current_operation == '-' and self.num1 < self.num2:
            self.num1, self.num2 = self.num2, self.num1
        self.correct_answer = self.num1 + self.num2 if self.current_operation == '+' else self.num1 - self.num2
        self.first_attempt = True

    def startQuiz(self):
        self.generateQuestion()
        self.displayProblem()

    def displayProblem(self):
        self.clearFrame()
        self.main_frame.configure(bg="#000000")

        tk.Label(self.main_frame,
                 text=f"Question {self.current_question + 1} of {self.total_questions}",
                 font=("Arial", 13, "bold"), fg="white", bg="#000000").pack(pady=5)
        
        tk.Label(self.main_frame, text=f"Score: {self.score}", font=("Arial", 13),
                 fg="#00FFAA", bg="#000000").pack(pady=5)
        
        problem_label = tk.Label(self.main_frame, text=f"{self.num1} {self.current_operation} {self.num2} = ?",
                                 font=("Arial", 22, "bold"), fg="#FFD700", bg="#000000")
        problem_label.pack(pady=20)
        
        self.answer_entry = tk.Entry(self.main_frame, font=("Arial", 16), width=10, justify="center")
        self.answer_entry.pack(pady=10)
        self.answer_entry.focus()
        self.answer_entry.bind('<Return>', lambda event: self.checkAnswer())
        
        tk.Button(self.main_frame, text="Submit Answer", command=self.checkAnswer,
                  bg="#28A745", fg="white", activebackground="#218838",
                  font=("Arial", 13, "bold"), width=15, bd=0, cursor="hand2").pack(pady=10)

    def checkAnswer(self):
        try:
            user_answer = int(self.answer_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a number.")
            return
        if user_answer == self.correct_answer:
            self.isCorrect(True)
        else:
            self.isCorrect(False)

    def isCorrect(self, correct):
        if correct:
            if self.first_attempt:
                self.score += 10
                messagebox.showinfo("✅ Correct!", "Well done! +10 points")
            else:
                self.score += 5
                messagebox.showinfo("✅ Correct!", "Good job! +5 points")
            self.nextQuestion()
        else:
            if self.first_attempt:
                self.first_attempt = False
                messagebox.showerror("❌ Incorrect", "That's not correct. Try again!")
                self.answer_entry.delete(0, tk.END)
                self.answer_entry.focus()
            else:
                messagebox.showerror("❌ Incorrect", f"Sorry, the answer was {self.correct_answer}.")
                self.nextQuestion()

    def nextQuestion(self):
        self.current_question += 1
        if self.current_question < self.total_questions:
            self.generateQuestion()
            self.displayProblem()
        else:
            self.displayResults()

    def displayResults(self):
        self.clearFrame()
        self.main_frame.configure(bg="#000000")
        grade = self.calculateGrade()

        tk.Label(self.main_frame, text="🏁 QUIZ COMPLETE 🏁", font=("Arial", 20, "bold"),
                 fg="white", bg="#000000").pack(pady=20)
        tk.Label(self.main_frame, text=f"Score: {self.score}/100", font=("Arial", 16),
                 fg="#00FFAA", bg="#000000").pack(pady=5)
        tk.Label(self.main_frame, text=f"Grade: {grade}", font=("Arial", 16, "bold"),
                 fg="#FFD700", bg="#000000").pack(pady=5)

        button_style = {"font": ("Arial", 13, "bold"), "width": 15, "cursor": "hand2", "bd": 0}
        tk.Button(self.main_frame, text="Play Again", bg="#0078D7", fg="white",
                  activebackground="#005A9E", command=self.displayMenu, **button_style).pack(pady=10)
        tk.Button(self.main_frame, text="Exit", bg="#DC3545", fg="white",
                  activebackground="#B02A37", command=self.root.quit, **button_style).pack(pady=10)

    def calculateGrade(self):
        if self.score >= 90: return "A+"
        elif self.score >= 80: return "A"
        elif self.score >= 70: return "B"
        elif self.score >= 60: return "C"
        elif self.score >= 50: return "D"
        else: return "F"


if __name__ == "__main__":
    root = tk.Tk()
    app = MathsQuiz(root)
    root.mainloop()
