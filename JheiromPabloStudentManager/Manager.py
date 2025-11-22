import os
import math
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, simpledialog

# -----------------------
# Data classes
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
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        self.students = []
        self.load_students()

    def load_students(self):
        self.students = []
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                if not lines:
                    return
                for line in lines[1:]:
                    data = line.strip().split(',')
                    if len(data) == 6:
                        self.students.append(Student(*data))
        except FileNotFoundError:
            with open(self.filename, 'w') as file:
                file.write("0\n")
        except Exception as e:
            messagebox.showerror("Error loading file", str(e))

    def save_students(self):
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
            self.students.append(Student(student_code, name, int(mark1), int(mark2), int(mark3), int(exam_mark)))
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
            for key in ['name', 'mark1', 'mark2', 'mark3', 'exam_mark']:
                if key in kwargs:
                    setattr(student, key, int(kwargs[key]) if 'mark' in key else kwargs[key])
            return True, "Student updated successfully"
        except ValueError:
            return False, "Invalid marks entered"

# -----------------------
# GUI App
# -----------------------
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager — Modern UI")
        self.root.geometry("1000x650")
        self.root.minsize(900, 600)

        self.manager = StudentManager()
        self.current_page = None

        # Layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self.root, width=220, corner_radius=8)
        self.sidebar.grid(row=0, column=0, sticky="nswe", padx=12, pady=12)
        self.sidebar.grid_rowconfigure(8, weight=1)

        self.header_frame = ctk.CTkFrame(self.root, height=80, corner_radius=8)
        self.header_frame.grid(row=0, column=1, sticky="new", padx=(0,12), pady=(12,0))
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self.root, corner_radius=8)
        self.main_frame.grid(row=1, column=1, sticky="nswe", padx=(0,12), pady=(12,12))
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Sidebar buttons
        self.logo = ctk.CTkLabel(self.sidebar, text="Student\nManager", font=ctk.CTkFont(size=18, weight="bold"))
        self.logo.grid(row=0, column=0, padx=12, pady=(12,8))

        self.btn_view_all = ctk.CTkButton(self.sidebar, text="View All", command=self.view_all_students)
        self.btn_view_all.grid(row=1, column=0, padx=12, pady=6, sticky="we")

        self.btn_individual = ctk.CTkButton(self.sidebar, text="Find Student", command=self.view_individual_student)
        self.btn_individual.grid(row=2, column=0, padx=12, pady=6, sticky="we")

        self.btn_add = ctk.CTkButton(self.sidebar, text="Add Student", command=self.add_student_dialog)
        self.btn_add.grid(row=3, column=0, padx=12, pady=6, sticky="we")

        self.btn_update = ctk.CTkButton(self.sidebar, text="Update Student", command=self.update_student_dialog)
        self.btn_update.grid(row=4, column=0, padx=12, pady=6, sticky="we")

        self.btn_delete = ctk.CTkButton(self.sidebar, text="Delete Student", command=self.delete_student)
        self.btn_delete.grid(row=5, column=0, padx=12, pady=6, sticky="we")

        self.btn_sort = ctk.CTkButton(self.sidebar, text="Sort Students", command=self.sort_students)
        self.btn_sort.grid(row=6, column=0, padx=12, pady=6, sticky="we")

        self.btn_refresh = ctk.CTkButton(self.sidebar, text="Refresh", command=self.refresh_data)
        self.btn_refresh.grid(row=7, column=0, padx=12, pady=6, sticky="we")

        # Theme toggle
        self.theme_toggle = ctk.CTkSegmentedButton(self.sidebar, values=["Light","Dark"], command=self.change_theme)
        self.theme_toggle.set("Dark")
        self.theme_toggle.grid(row=9, column=0, padx=12, pady=10, sticky="we")

        # Header animation
        self.header_label = ctk.CTkLabel(self.header_frame, text="Student Records", font=ctk.CTkFont(size=22, weight="bold"))
        self.header_label.place(x=900, y=18)
        self.header_animation_step = 0
        self.animate_header_slide_in()

        self.shimmer_angle = 0
        self.animate_shimmer()

        # Pulse Add button
        self.pulse_state = 0
        self.animate_pulse_button()

        # Initial page
        self.display_welcome_page()

    # ----------------- Page system -----------------
    def create_text_page(self, title, initial_text=""):
        page = ctk.CTkFrame(self.main_frame, corner_radius=8)
        page.grid(row=0, column=0, sticky="nswe")
        page.grid_rowconfigure(0, weight=1)
        page.grid_columnconfigure(0, weight=1)

        text_output = ctk.CTkTextbox(page, width=600, height=400, corner_radius=6, wrap="word")
        text_output.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)
        text_output.insert("0.0", initial_text)

        scrollbar = ctk.CTkScrollbar(page, command=text_output.yview)
        scrollbar.grid(row=0, column=1, sticky="ns", padx=(0,12), pady=12)
        text_output.configure(yscrollcommand=scrollbar.set)

        return page, text_output

    def show_page(self, page):
        if self.current_page:
            old_page = self.current_page
            def slide_out(step=0):
                if step < 20:
                    old_page.place(x=-int((step/20)*self.main_frame.winfo_width()), y=0)
                    self.root.after(12, lambda: slide_out(step+1))
                else:
                    old_page.place_forget()
            slide_out()

        self.current_page = page
        page.place(x=self.main_frame.winfo_width(), y=0, relwidth=1, relheight=1)
        def slide_in(step=0):
            if step <= 20:
                new_x = int(self.main_frame.winfo_width()*(1 - step/20))
                page.place(x=new_x, y=0, relwidth=1, relheight=1)
                self.root.after(12, lambda: slide_in(step+1))
            else:
                page.place(x=0, y=0, relwidth=1, relheight=1)
        slide_in()

    # ----------------- Animations -----------------
    def animate_header_slide_in(self):
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
        def step():
            geo = dialog.geometry()
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
        self.pulse_state += 0.06
        val = (math.sin(self.pulse_state) + 1) / 2
        try:
            if val > 0.7:
                self.btn_add.configure(font=ctk.CTkFont(size=13, weight="bold"))
            else:
                self.btn_add.configure(font=ctk.CTkFont(size=12, weight="normal"))
        except Exception:
            pass
        self.root.after(120, self.animate_pulse_button)

    def animate_shimmer(self):
        self.shimmer_angle = (self.shimmer_angle + 1) % 40
        dots = "." * (self.shimmer_angle // 10)
        self.header_label.configure(text=f"Student Records {dots}")
        self.root.after(300, self.animate_shimmer)

    # ----------------- Theme -----------------
    def change_theme(self, new_mode):
        ctk.set_appearance_mode(new_mode)

    # ----------------- Utility -----------------
    def format_student_output(self, student):
        return (f"Name: {student.name}\n"
                f"Student Code: {student.student_code}\n"
                f"Total Coursework: {student.total_coursework}/60\n"
                f"Exam Mark: {student.exam_mark}/100\n"
                f"Overall Percentage: {student.overall_percentage:.2f}%\n"
                f"Grade: {student.grade}\n"
                f"{'-'*50}\n")

    # ----------------- Pages -----------------
    def display_welcome_page(self):
        page, text_output = self.create_text_page("Welcome",
            "Welcome to Student Manager — Modern UI with animations.\nUse the sidebar to interact with records.")
        self.show_page(page)

    def refresh_data(self):
        self.manager.load_students()
        self.display_welcome_page()

    def view_all_students(self):
        students = self.manager.get_all_students()
        output_text = ""
        if not students:
            output_text = "No students found."
        else:
            output_text += "ALL STUDENT RECORDS\n" + "="*50 + "\n"
            total_percentage = 0
            for student in students:
                output_text += self.format_student_output(student)
                total_percentage += student.overall_percentage
            average_percentage = total_percentage / len(students)
            output_text += f"SUMMARY:\nNumber of students: {len(students)}\nAverage percentage: {average_percentage:.2f}%"

        page, text_output = self.create_text_page("All Students", initial_text=output_text)
        self.show_page(page)

    def view_individual_student(self):
        code = simpledialog.askstring("Find Student", "Enter Student Code:")
        if not code:
            return
        student = self.manager.get_student_by_code(code)
        output_text = ""
        if student:
            output_text += "INDIVIDUAL STUDENT RECORD\n" + "="*50 + "\n"
            output_text += self.format_student_output(student)
        else:
            output_text = "Student not found."
        page, text_output = self.create_text_page("Individual Student", initial_text=output_text)
        self.show_page(page)

    def sort_students(self):
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
        output_text = title + "\n" + "="*50 + "\n"
        for s in students:
            output_text += self.format_student_output(s)
        page, text_output = self.create_text_page("Sorted Students", initial_text=output_text)
        self.show_page(page)

    # ----------------- Add / Update / Delete -----------------
    def add_student_dialog(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Add Student")
        dialog.geometry("380x360")
        dialog.transient(self.root)
        dialog.grab_set()
        # Float-in animation
        screen_w = dialog.winfo_screenwidth()
        screen_h = dialog.winfo_screenheight()
        x = (screen_w // 2) - 190
        y = (screen_h // 2) + 200
        dialog.geometry(f"+{x}+{y}")
        self.animate_dialog_ascend(dialog, target_y=(screen_h // 2) - 180)

        # Form
        labels = ["Student Code","Name","Course Mark 1 (0-20)","Course Mark 2 (0-20)","Course Mark 3 (0-20)","Exam Mark (0-100)"]
        entries = []
        for i, label in enumerate(labels):
            ctk.CTkLabel(dialog, text=label).grid(row=i, column=0, padx=12, pady=8, sticky="w")
            entry = ctk.CTkEntry(dialog)
            entry.grid(row=i, column=1, padx=12, pady=8)
            entries.append(entry)

        def submit():
            success, message = self.manager.add_student(*(e.get() for e in entries))
            if success:
                if self.manager.save_students():
                    messagebox.showinfo("Success", message)
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to save!")
            else:
                messagebox.showerror("Error", message)

        ctk.CTkButton(dialog, text="Add Student", command=submit).grid(row=6, column=0, columnspan=2, pady=16, padx=12, sticky="we")

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
                    messagebox.showerror("Error", "Failed to save!")
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
        dialog.geometry("380x320")
        dialog.transient(self.root)
        dialog.grab_set()
        screen_w = dialog.winfo_screenwidth()
        screen_h = dialog.winfo_screenheight()
        x = (screen_w // 2) - 190
        y = (screen_h // 2) + 200
        dialog.geometry(f"+{x}+{y}")
        self.animate_dialog_ascend(dialog, target_y=(screen_h // 2) - 160)

        labels = ["Name","Course Mark 1","Course Mark 2","Course Mark 3","Exam Mark"]
        default_vals = [student.name, student.mark1, student.mark2, student.mark3, student.exam_mark]
        entries = []
        for i, (label, val) in enumerate(zip(labels, default_vals)):
            ctk.CTkLabel(dialog, text=label).grid(row=i, column=0, padx=12, pady=8, sticky="w")
            entry = ctk.CTkEntry(dialog)
            entry.insert(0, str(val))
            entry.grid(row=i, column=1, padx=12, pady=8)
            entries.append(entry)

        def submit():
            kwargs = {k:v.get() for k,v in zip(['name','mark1','mark2','mark3','exam_mark'], entries)}
            success, message = self.manager.update_student(code, **kwargs)
            if success:
                if self.manager.save_students():
                    messagebox.showinfo("Success", message)
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to save!")
            else:
                messagebox.showerror("Error", message)

        ctk.CTkButton(dialog, text="Update Student", command=submit).grid(row=5, column=0, columnspan=2, pady=16, padx=12, sticky="we")


if __name__ == "__main__":
    root = ctk.CTk()
    app = StudentManagerApp(root)
    root.mainloop()
