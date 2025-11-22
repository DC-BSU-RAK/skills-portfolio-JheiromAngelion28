import os
import math
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, simpledialog

# -----------------------
# Data classes (unchanged logic)
# -----------------------
class Student:
    def __init__(self, student_code, name, mark1, mark2, mark3, exam_mark):
        self.student_code = student_code
        self.name = name
        self.mark1 = int(mark1)
        self.mark2 = int(mark2)
        self.mark3 = int(mark3)
        self.exam_mark = int(exam_mark)

    @property
    def total_coursework(self):
        return self.mark1 + self.mark2 + self.mark3

    @property
    def overall_percentage(self):
        total_marks = self.total_coursework + self.exam_mark
        # total possible = 60 coursework + 100 exam = 160
        return (total_marks / 160) * 100

    @property
    def grade(self):
        percentage = self.overall_percentage
        if percentage >= 70:
            return 'A'
        elif percentage >= 60:
            return 'B'
        elif percentage >= 50:
            return 'C'
        elif percentage >= 40:
            return 'D'
        else:
            return 'F'

    def to_file_string(self):
        return f"{self.student_code},{self.name},{self.mark1},{self.mark2},{self.mark3},{self.exam_mark}"


class StudentManager:
    def __init__(self, filename="JheiromPabloStudentManager/studentMarks.txt"):
        self.filename = filename
        # ensure folder exists
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        self.students = []
        self.load_students()

    def load_students(self):
        """Load students from file"""
        self.students = []
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                if not lines:
                    return
                # Skip first line (count)
                for line in lines[1:]:
                    data = line.strip().split(',')
                    if len(data) == 6:
                        student = Student(data[0], data[1], data[2], data[3], data[4], data[5])
                        self.students.append(student)
        except FileNotFoundError:
            # create empty file if missing
            with open(self.filename, 'w') as file:
                file.write("0\n")
        except Exception as e:
            messagebox.showerror("Error loading file", str(e))

    def save_students(self):
        """Save students to file"""
        try:
            with open(self.filename, 'w') as file:
                file.write(f"{len(self.students)}\n")
                for student in self.students:
                    file.write(student.to_file_string() + "\n")
            return True
        except Exception as e:
            messagebox.showerror("Error saving file", str(e))
            return False

    def get_all_students(self):
        return self.students

    def get_student_by_code(self, code):
        for student in self.students:
            if student.student_code == code:
                return student
        return None

    def get_student_by_name(self, name):
        matches = []
        for student in self.students:
            if name.lower() in student.name.lower():
                matches.append(student)
        return matches

    def get_highest_scoring_student(self):
        if not self.students:
            return None
        return max(self.students, key=lambda x: x.overall_percentage)

    def get_lowest_scoring_student(self):
        if not self.students:
            return None
        return min(self.students, key=lambda x: x.overall_percentage)

    def add_student(self, student_code, name, mark1, mark2, mark3, exam_mark):
        if self.get_student_by_code(student_code):
            return False, "Student code already exists"
        try:
            student = Student(student_code, name, int(mark1), int(mark2), int(mark3), int(exam_mark))
            self.students.append(student)
            return True, "Student added successfully"
        except ValueError:
            return False, "Invalid marks entered"

    def delete_student(self, student_code):
        student = self.get_student_by_code(student_code)
        if student:
            self.students.remove(student)
            return True, "Student deleted successfully"
        return False, "Student not found"

    def update_student(self, student_code, **kwargs):
        student = self.get_student_by_code(student_code)
        if not student:
            return False, "Student not found"
        try:
            if 'name' in kwargs:
                student.name = kwargs['name']
            if 'mark1' in kwargs:
                student.mark1 = int(kwargs['mark1'])
            if 'mark2' in kwargs:
                student.mark2 = int(kwargs['mark2'])
            if 'mark3' in kwargs:
                student.mark3 = int(kwargs['mark3'])
            if 'exam_mark' in kwargs:
                student.exam_mark = int(kwargs['exam_mark'])
            return True, "Student updated successfully"
        except ValueError:
            return False, "Invalid marks entered"

# -----------------------
# GUI App (CustomTkinter)
# -----------------------

# Setup CustomTkinter appearance
ctk.set_appearance_mode("Dark")               # start in dark mode by default
ctk.set_default_color_theme("blue")           # builtin blue theme (works nicely with light/dark)

class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager — Modern (customtkinter)")
        self.root.geometry("1000x650")
        # Allow resizing
        self.root.minsize(900, 600)

        self.manager = StudentManager()

        # Root grid configuration
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Sidebar (left)
        self.sidebar = ctk.CTkFrame(self.root, width=220, corner_radius=8)
        self.sidebar.grid(row=0, column=0, sticky="nswe", padx=12, pady=12)
        self.sidebar.grid_rowconfigure(8, weight=1)

        # Header area (top of main)
        self.header_frame = ctk.CTkFrame(self.root, height=80, corner_radius=8)
        self.header_frame.grid(row=0, column=1, sticky="new", padx=(0,12), pady=(12,0))
        self.header_frame.grid_columnconfigure(0, weight=1)

        # Main content frame (below header)
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=8)
        self.main_frame.grid(row=1, column=1, sticky="nswe", padx=(0,12), pady=(12,12))
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # ---------------- Sidebar widgets ----------------
        self.logo = ctk.CTkLabel(self.sidebar, text="Student\nManager", font=ctk.CTkFont(size=18, weight="bold"))
        self.logo.grid(row=0, column=0, padx=12, pady=(12,8))

        self.btn_view_all = ctk.CTkButton(self.sidebar, text="View All", command=self.view_all_students, corner_radius=6)
        self.btn_view_all.grid(row=1, column=0, padx=12, pady=6, sticky="we")

        self.btn_individual = ctk.CTkButton(self.sidebar, text="Find Student", command=self.view_individual_student, corner_radius=6)
        self.btn_individual.grid(row=2, column=0, padx=12, pady=6, sticky="we")

        self.btn_add = ctk.CTkButton(self.sidebar, text="Add Student", command=self.add_student_dialog, corner_radius=8)
        self.btn_add.grid(row=3, column=0, padx=12, pady=6, sticky="we")

        self.btn_update = ctk.CTkButton(self.sidebar, text="Update Student", command=self.update_student_dialog, corner_radius=8)
        self.btn_update.grid(row=4, column=0, padx=12, pady=6, sticky="we")

        self.btn_delete = ctk.CTkButton(self.sidebar, text="Delete Student", command=self.delete_student, corner_radius=8)
        self.btn_delete.grid(row=5, column=0, padx=12, pady=6, sticky="we")

        self.btn_sort = ctk.CTkButton(self.sidebar, text="Sort Students", command=self.sort_students, corner_radius=8)
        self.btn_sort.grid(row=6, column=0, padx=12, pady=6, sticky="we")

        self.btn_refresh = ctk.CTkButton(self.sidebar, text="Refresh", command=self.refresh_data, corner_radius=8)
        self.btn_refresh.grid(row=7, column=0, padx=12, pady=6, sticky="we")

        # Theme toggle (light / dark)
        self.theme_var = ctk.StringVar(value="Dark")
        self.theme_toggle = ctk.CTkSegmentedButton(self.sidebar, values=["Light", "Dark"], command=self.change_theme)
        self.theme_toggle.set("Dark")
        self.theme_toggle.grid(row=9, column=0, padx=12, pady=10, sticky="we")

        # ---------------- Header widgets + animation state ----------------
        self.header_label = ctk.CTkLabel(self.header_frame, text="Student Records", font=ctk.CTkFont(size=22, weight="bold"))
        # We'll place header using place to animate slide-in
        self.header_label.place(x=900, y=18)  # start off-screen (right)
        self.header_animation_step = 0
        self.animate_header_slide_in()

        # subtle shimmer effect variables
        self.shimmer_angle = 0
        self.animate_shimmer()

        # ---------------- Main content: Text output in a CTkTextbox ----------------
        # CTkTextbox available in modern customtkinter; fallback to tk.Text if not present
        try:
            self.text_output = ctk.CTkTextbox(self.main_frame, width=600, height=400, corner_radius=6, wrap="word")
            self.text_output.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)
        except Exception:
            # fallback to tk.Text inside CTkFrame
            self.text_output = tk.Text(self.main_frame, wrap="word")
            self.text_output.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)

        # scroll bar for the text area
        self.scrollbar = ctk.CTkScrollbar(self.main_frame, command=self.on_scroll)
        self.scrollbar.grid(row=0, column=1, sticky="ns", padx=(0,12), pady=12)
        # attach scrollbar to ctkttextbox or tk.Text
        try:
            self.text_output.configure(yscrollcommand=self.scrollbar.set)
        except Exception:
            self.text_output.configure(yscrollcommand=self.scrollbar.set)

        # small footer label
        self.footer = ctk.CTkLabel(self.main_frame, text="Ready", anchor="w")
        self.footer.grid(row=1, column=0, sticky="we", padx=12, pady=(0,12))

        # Add a pulsing animation to the Add button to draw attention
        self.pulse_state = 0
        self.animate_pulse_button()

        # Show initial welcome text
        self.clear_output()
        self.display_text("Welcome to Student Manager — Modern UI with animations.\nUse the sidebar to interact with records.")

    # ----------------- Utility / display methods -----------------
    def on_scroll(self, *args):
        try:
            self.text_output.yview(*args)
        except Exception:
            pass

    def clear_output(self):
        try:
            self.text_output.delete("0.0", tk.END)
        except Exception:
            self.text_output.delete(1.0, tk.END)

    def display_text(self, text):
        try:
            self.text_output.insert(tk.END, text + "\n")
            self.text_output.see(tk.END)
        except Exception:
            self.text_output.insert("end", text + "\n")
            self.text_output.see("end")

    def format_student_output(self, student):
        return (f"Name: {student.name}\n"
                f"Student Code: {student.student_code}\n"
                f"Total Coursework: {student.total_coursework}/60\n"
                f"Exam Mark: {student.exam_mark}/100\n"
                f"Overall Percentage: {student.overall_percentage:.2f}%\n"
                f"Grade: {student.grade}\n"
                f"{'-'*50}\n")

    # ----------------- Actions -----------------
    def refresh_data(self):
        self.manager.load_students()
        self.clear_output()
        self.display_text("Data refreshed from file.")

    def view_all_students(self):
        self.clear_output()
        students = self.manager.get_all_students()
        if not students:
            self.display_text("No students found.")
            return
        self.display_text("ALL STUDENT RECORDS")
        self.display_text("=" * 50)
        total_percentage = 0
        for student in students:
            self.display_text(self.format_student_output(student))
            total_percentage += student.overall_percentage
        average_percentage = total_percentage / len(students)
        self.display_text("SUMMARY:")
        self.display_text(f"Number of students: {len(students)}")
        self.display_text(f"Average percentage: {average_percentage:.2f}%")

    def view_individual_student(self):
        code = simpledialog.askstring("Find Student", "Enter Student Code:")
        if code:
            student = self.manager.get_student_by_code(code)
            if student:
                self.clear_output()
                self.display_text("INDIVIDUAL STUDENT RECORD")
                self.display_text("=" * 50)
                self.display_text(self.format_student_output(student))
            else:
                messagebox.showerror("Not found", "Student not found!")

    def show_highest_student(self):
        student = self.manager.get_highest_scoring_student()
        self.clear_output()
        if student:
            self.display_text("HIGHEST SCORING STUDENT")
            self.display_text("=" * 50)
            self.display_text(self.format_student_output(student))
        else:
            self.display_text("No students found.")

    def show_lowest_student(self):
        student = self.manager.get_lowest_scoring_student()
        self.clear_output()
        if student:
            self.display_text("LOWEST SCORING STUDENT")
            self.display_text("=" * 50)
            self.display_text(self.format_student_output(student))
        else:
            self.display_text("No students found.")

    def sort_students(self):
        # Simple choice dialog
        choice = simpledialog.askstring("Sort Students",
                                        "Sort by:\n1 - Name (A-Z)\n2 - Name (Z-A)\n3 - Percentage (High-Low)\n4 - Percentage (Low-High)")
        students = self.manager.get_all_students()
        if not students:
            messagebox.showinfo("Info", "No students to sort.")
            return
        if choice == "1":
            students.sort(key=lambda x: x.name)
            title = "STUDENTS SORTED BY NAME (A-Z)"
        elif choice == "2":
            students.sort(key=lambda x: x.name, reverse=True)
            title = "STUDENTS SORTED BY NAME (Z-A)"
        elif choice == "3":
            students.sort(key=lambda x: x.overall_percentage, reverse=True)
            title = "STUDENTS SORTED BY PERCENTAGE (HIGH-LOW)"
        elif choice == "4":
            students.sort(key=lambda x: x.overall_percentage)
            title = "STUDENTS SORTED BY PERCENTAGE (LOW-HIGH)"
        else:
            messagebox.showerror("Invalid", "Invalid sort option!")
            return
        self.clear_output()
        self.display_text(title)
        self.display_text("=" * 50)
        for s in students:
            self.display_text(self.format_student_output(s))

    def add_student_dialog(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Add Student")
        dialog.geometry("380x360")
        dialog.transient(self.root)
        dialog.grab_set()

        # simple float-in animation (start below and move up)
        dialog.update_idletasks()
        screen_w = dialog.winfo_screenwidth()
        screen_h = dialog.winfo_screenheight()
        x = (screen_w // 2) - 190
        y = (screen_h // 2) + 200  # start lower
        dialog.geometry(f"+{x}+{y}")
        # animate up
        self.animate_dialog_ascend(dialog, target_y=(screen_h // 2) - 180)

        # form fields
        padding_y = 8
        ctk.CTkLabel(dialog, text="Student Code:").grid(row=0, column=0, padx=12, pady=padding_y, sticky="w")
        code_entry = ctk.CTkEntry(dialog)
        code_entry.grid(row=0, column=1, padx=12, pady=padding_y)

        ctk.CTkLabel(dialog, text="Name:").grid(row=1, column=0, padx=12, pady=padding_y, sticky="w")
        name_entry = ctk.CTkEntry(dialog)
        name_entry.grid(row=1, column=1, padx=12, pady=padding_y)

        ctk.CTkLabel(dialog, text="Course Mark 1 (0-20):").grid(row=2, column=0, padx=12, pady=padding_y, sticky="w")
        mark1_entry = ctk.CTkEntry(dialog)
        mark1_entry.grid(row=2, column=1, padx=12, pady=padding_y)

        ctk.CTkLabel(dialog, text="Course Mark 2 (0-20):").grid(row=3, column=0, padx=12, pady=padding_y, sticky="w")
        mark2_entry = ctk.CTkEntry(dialog)
        mark2_entry.grid(row=3, column=1, padx=12, pady=padding_y)

        ctk.CTkLabel(dialog, text="Course Mark 3 (0-20):").grid(row=4, column=0, padx=12, pady=padding_y, sticky="w")
        mark3_entry = ctk.CTkEntry(dialog)
        mark3_entry.grid(row=4, column=1, padx=12, pady=padding_y)

        ctk.CTkLabel(dialog, text="Exam Mark (0-100):").grid(row=5, column=0, padx=12, pady=padding_y, sticky="w")
        exam_entry = ctk.CTkEntry(dialog)
        exam_entry.grid(row=5, column=1, padx=12, pady=padding_y)

        def submit():
            success, message = self.manager.add_student(
                code_entry.get(), name_entry.get(),
                mark1_entry.get(), mark2_entry.get(), mark3_entry.get(), exam_entry.get()
            )
            if success:
                if self.manager.save_students():
                    messagebox.showinfo("Success", message)
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to save to file!")
            else:
                messagebox.showerror("Error", message)

        submit_btn = ctk.CTkButton(dialog, text="Add Student", command=submit)
        submit_btn.grid(row=6, column=0, columnspan=2, pady=16, padx=12, sticky="we")

    def delete_student(self):
        code = simpledialog.askstring("Delete Student", "Enter Student Code to delete:")
        if not code:
            return
        student = self.manager.get_student_by_code(code)
        if not student:
            messagebox.showerror("Not found", "Student not found!")
            return
        confirm = messagebox.askyesno("Confirm", f"Delete {student.name}?")
        if confirm:
            success, message = self.manager.delete_student(code)
            if success:
                if self.manager.save_students():
                    messagebox.showinfo("Success", message)
                else:
                    messagebox.showerror("Error", "Failed to save to file!")
            else:
                messagebox.showerror("Error", message)

    def update_student_dialog(self):
        code = simpledialog.askstring("Update Student", "Enter Student Code:")
        if not code:
            return
        student = self.manager.get_student_by_code(code)
        if not student:
            messagebox.showerror("Not found", "Student not found!")
            return

        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Update Student")
        dialog.geometry("380x340")
        dialog.transient(self.root)
        dialog.grab_set()
        # float-in animation
        dialog.update_idletasks()
        screen_w = dialog.winfo_screenwidth()
        screen_h = dialog.winfo_screenheight()
        x = (screen_w // 2) - 190
        y = (screen_h // 2) + 200
        dialog.geometry(f"+{x}+{y}")
        self.animate_dialog_ascend(dialog, target_y=(screen_h // 2) - 180)

        ctk.CTkLabel(dialog, text=f"Updating: {student.name}").grid(row=0, column=0, columnspan=2, padx=12, pady=10)

        ctk.CTkLabel(dialog, text="New Name:").grid(row=1, column=0, padx=12, pady=6, sticky="w")
        name_entry = ctk.CTkEntry(dialog)
        name_entry.insert(0, student.name)
        name_entry.grid(row=1, column=1, padx=12, pady=6)

        ctk.CTkLabel(dialog, text="Course Mark 1:").grid(row=2, column=0, padx=12, pady=6, sticky="w")
        mark1_entry = ctk.CTkEntry(dialog)
        mark1_entry.insert(0, str(student.mark1))
        mark1_entry.grid(row=2, column=1, padx=12, pady=6)

        ctk.CTkLabel(dialog, text="Course Mark 2:").grid(row=3, column=0, padx=12, pady=6, sticky="w")
        mark2_entry = ctk.CTkEntry(dialog)
        mark2_entry.insert(0, str(student.mark2))
        mark2_entry.grid(row=3, column=1, padx=12, pady=6)

        ctk.CTkLabel(dialog, text="Course Mark 3:").grid(row=4, column=0, padx=12, pady=6, sticky="w")
        mark3_entry = ctk.CTkEntry(dialog)
        mark3_entry.insert(0, str(student.mark3))
        mark3_entry.grid(row=4, column=1, padx=12, pady=6)

        ctk.CTkLabel(dialog, text="Exam Mark:").grid(row=5, column=0, padx=12, pady=6, sticky="w")
        exam_entry = ctk.CTkEntry(dialog)
        exam_entry.insert(0, str(student.exam_mark))
        exam_entry.grid(row=5, column=1, padx=12, pady=6)

        def submit():
            success, message = self.manager.update_student(
                code,
                name=name_entry.get(),
                mark1=mark1_entry.get(),
                mark2=mark2_entry.get(),
                mark3=mark3_entry.get(),
                exam_mark=exam_entry.get()
            )
            if success:
                if self.manager.save_students():
                    messagebox.showinfo("Success", message)
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to save to file!")
            else:
                messagebox.showerror("Error", message)

        ctk.CTkButton(dialog, text="Update Student", command=submit).grid(row=6, column=0, columnspan=2, pady=12, padx=12, sticky="we")

    # ----------------- Animations -----------------

    def animate_header_slide_in(self):
        """Slide header from right to its target position"""
        # compute current x, target x
        cur = self.header_label.winfo_x()
        target_x = 20
        if cur > target_x:
            step = max(1, (cur - target_x) // 8)
            new_x = cur - step
            self.header_label.place(x=new_x, y=18)
            self.root.after(18, self.animate_header_slide_in)
        else:
            self.header_label.place(x=target_x, y=18)

    def animate_dialog_ascend(self, dialog, target_y, speed=12):
        """Animate a Toplevel dialog rising into the centre"""
        def step():
            geo = dialog.geometry()
            # geometry example: "380x360+100+200"
            parts = geo.split('+')
            if len(parts) >= 3:
                try:
                    cur_y = int(parts[2])
                except Exception:
                    cur_y = target_y + 200
            else:
                cur_y = dialog.winfo_y()
            if cur_y > target_y:
                new_y = max(target_y, cur_y - speed)
                dialog.geometry(f"+{dialog.winfo_x()}+{new_y}")
                dialog.after(12, step)
            else:
                dialog.geometry(f"+{dialog.winfo_x()}+{target_y}")
        step()

    def animate_pulse_button(self):
        """Pulse effect on Add button by changing its alpha/lightness"""
        # pulse between 0 and 1
        self.pulse_state += 0.06
        val = (math.sin(self.pulse_state) + 1) / 2  # 0..1
        # compute a slightly lighter/darker color by changing fg_color via configure
        # customtkinter doesn't accept direct color animation for buttons easily,
        # but we can alternate the button's hover color using configure
        try:
            base = ctk.ThemeManager.theme["CTkButton"]["fg_color"]
            # just toggle between two states by adjusting opacity-like behavior (workaround)
            if val > 0.7:
                # emphasize
                self.btn_add.configure(font=ctk.CTkFont(size=13, weight="bold"))
            else:
                self.btn_add.configure(font=ctk.CTkFont(size=12, weight="normal"))
        except Exception:
            pass
        # repeat
        self.root.after(120, self.animate_pulse_button)

    def animate_shimmer(self):
        """Small shimmer effect for header text color/tranform"""
        # rotate through a subtle hue offset by adjusting label color via fg_color not directly supported.
        # We'll slightly change the text to simulate shimmer by adding a dot that moves.
        self.shimmer_angle = (self.shimmer_angle + 1) % 40
        dots = "." * (self.shimmer_angle // 10)
        self.header_label.configure(text=f"Student Records {dots}")
        self.root.after(300, self.animate_shimmer)

    # ---------------- Theme control ----------------
    def change_theme(self, new_mode):
        if new_mode == "Light":
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")

    # ----------------- Other helpers (not animations) -----------------

def main():
    root = ctk.CTk()
    app = StudentManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
