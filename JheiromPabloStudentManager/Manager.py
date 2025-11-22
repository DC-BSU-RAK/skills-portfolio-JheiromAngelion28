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
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        self.students = []
        self.load_students()

    def load_students(self):
        self.students = []
        try:
            # Check if file exists and has content
            if not os.path.exists(self.filename):
                # Create file with initial count of 0
                with open(self.filename, 'w') as file:
                    file.write("0\n")
                return
                
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                if not lines: 
                    return
                
                # Read the count from first line
                try:
                    count = int(lines[0].strip())
                except ValueError:
                    count = 0
                
                # Load students from subsequent lines
                for line in lines[1:]:
                    data = line.strip().split(',')
                    if len(data) == 6:
                        student = Student(*data)
                        self.students.append(student)
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

    def add_student(self, student_code, name, mark1, mark2, mark3, exam_mark):
        if self.get_student_by_code(student_code):
            return False, "Student code already exists"
        try:
            # Validate marks range
            marks = [int(mark1), int(mark2), int(mark3), int(exam_mark)]
            if any(m < 0 for m in marks):
                return False, "Marks cannot be negative"
            if marks[0] > 20 or marks[1] > 20 or marks[2] > 20:
                return False, "Course marks must be between 0-20"
            if marks[3] > 100:
                return False, "Exam mark must be between 0-100"
                
            student = Student(student_code, name, marks[0], marks[1], marks[2], marks[3])
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
                mark = int(kwargs['mark1'])
                if mark < 0 or mark > 20:
                    return False, "Course mark 1 must be between 0-20"
                student.mark1 = mark
            if 'mark2' in kwargs: 
                mark = int(kwargs['mark2'])
                if mark < 0 or mark > 20:
                    return False, "Course mark 2 must be between 0-20"
                student.mark2 = mark
            if 'mark3' in kwargs: 
                mark = int(kwargs['mark3'])
                if mark < 0 or mark > 20:
                    return False, "Course mark 3 must be between 0-20"
                student.mark3 = mark
            if 'exam_mark' in kwargs: 
                mark = int(kwargs['exam_mark'])
                if mark < 0 or mark > 100:
                    return False, "Exam mark must be between 0-100"
                student.exam_mark = mark
            return True, "Student updated successfully"
        except ValueError:
            return False, "Invalid marks entered"

    def get_highest_scoring_student(self):
        if not self.students: return None
        return max(self.students, key=lambda x: x.overall_percentage)

    def get_lowest_scoring_student(self):
        if not self.students: return None
        return min(self.students, key=lambda x: x.overall_percentage)

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
        self.root.minsize(900,600)

        self.manager = StudentManager()

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

        self.theme_toggle = ctk.CTkSegmentedButton(self.sidebar, values=["Light","Dark"], command=self.change_theme)
        self.theme_toggle.set("Dark")
        self.theme_toggle.grid(row=9,column=0, padx=12,pady=10, sticky="we")

        self.header_label = ctk.CTkLabel(self.header_frame, text="Student Records", font=ctk.CTkFont(size=22, weight="bold"))
        self.header_label.place(x=20, y=18)

        # Initial page
        self.show_welcome()

    # ----------------- Modern Card Functions -----------------
    def create_student_card(self, parent, student):
        grade_colors = {"A":"#4CAF50", "B":"#8BC34A", "C":"#FFC107", "D":"#FF9800", "F":"#F44336"}
        card = ctk.CTkFrame(parent, corner_radius=12, border_width=1, border_color="#4D4D4D")
        card.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(card, text=student.name, font=ctk.CTkFont(size=16, weight="bold")).grid(row=0,column=0,sticky="w", padx=12, pady=(8,2))
        ctk.CTkLabel(card, text=f"Code: {student.student_code}", font=ctk.CTkFont(size=12)).grid(row=1,column=0, sticky="w", padx=12)
        marks_text = (f"Coursework: {student.total_coursework}/60\n"
                      f"Exam: {student.exam_mark}/100\n"
                      f"Overall: {student.overall_percentage:.2f}%")
        ctk.CTkLabel(card, text=marks_text, font=ctk.CTkFont(size=12)).grid(row=2,column=0, sticky="w", padx=12, pady=2)
        ctk.CTkLabel(card, text=f"Grade: {student.grade}", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=grade_colors.get(student.grade, "#FFFFFF")).grid(row=3,column=0, sticky="w", padx=12, pady=(0,8))
        return card

    def display_students_cards(self, students, title="Students"):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        page = ctk.CTkFrame(self.main_frame, corner_radius=8)
        page.grid(row=0, column=0, sticky="nswe")
        page.grid_columnconfigure(0, weight=1)

        # Scrollable frame using CTkScrollableFrame instead of Canvas
        scrollable_frame = ctk.CTkScrollableFrame(page)
        scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        scrollable_frame.grid_columnconfigure(0, weight=1)

        header = ctk.CTkLabel(scrollable_frame, text=title, font=ctk.CTkFont(size=20, weight="bold"))
        header.grid(row=0, column=0, pady=12, sticky="w")
        
        if not students:
            no_data_label = ctk.CTkLabel(scrollable_frame, text="No students found", font=ctk.CTkFont(size=14))
            no_data_label.grid(row=1, column=0, pady=20, sticky="w")
            return
            
        for i, student in enumerate(students):
            card = self.create_student_card(scrollable_frame, student)
            card.grid(row=i+1, column=0, sticky="we", pady=8)

    def show_welcome(self):
        # Show some statistics or welcome message instead of empty cards
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        welcome_frame = ctk.CTkFrame(self.main_frame, corner_radius=8)
        welcome_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(welcome_frame, text="Welcome to Student Manager", 
                     font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        
        stats_text = f"Total Students: {len(self.manager.students)}"
        ctk.CTkLabel(welcome_frame, text=stats_text, 
                     font=ctk.CTkFont(size=16)).pack(pady=10)
        
        if self.manager.students:
            highest = self.manager.get_highest_scoring_student()
            lowest = self.manager.get_lowest_scoring_student()
            
            high_text = f"Highest Score: {highest.name} - {highest.overall_percentage:.2f}%"
            low_text = f"Lowest Score: {lowest.name} - {lowest.overall_percentage:.2f}%"
            
            ctk.CTkLabel(welcome_frame, text=high_text, 
                         font=ctk.CTkFont(size=14)).pack(pady=5)
            ctk.CTkLabel(welcome_frame, text=low_text, 
                         font=ctk.CTkFont(size=14)).pack(pady=5)

    # ----------------- Actions -----------------
    def refresh_data(self):
        self.manager.load_students()
        self.show_welcome()
        messagebox.showinfo("Info","Data refreshed from file.")

    def view_all_students(self):
        students = self.manager.get_all_students()
        if not students:
            messagebox.showinfo("Info","No students found.")
            return
        self.display_students_cards(students, title="All Students")

    def view_individual_student(self):
        code = simpledialog.askstring("Find Student", "Enter Student Code:")
        if not code: return
        student = self.manager.get_student_by_code(code)
        if not student:
            messagebox.showerror("Not found", "Student not found!")
            return
        self.display_students_cards([student], title=f"Student: {student.name}")

    def add_student_dialog(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Add Student")
        dialog.geometry("380x360")
        dialog.transient(self.root)
        dialog.grab_set()

        labels = ["Student Code","Name","Course Mark 1 (0-20)","Course Mark 2 (0-20)","Course Mark 3 (0-20)","Exam Mark (0-100)"]
        entries = []
        for i,text in enumerate(labels):
            ctk.CTkLabel(dialog, text=text).grid(row=i, column=0, padx=12,pady=6, sticky="w")
            e = ctk.CTkEntry(dialog)
            e.grid(row=i,column=1,padx=12,pady=6)
            entries.append(e)

        def submit():
            # Validate required fields
            if not all(entries[i].get() for i in [0, 1]):  # Code and Name are required
                messagebox.showerror("Error", "Student Code and Name are required!")
                return
                
            success, message = self.manager.add_student(
                entries[0].get(), entries[1].get(),
                entries[2].get() or "0",  # Default to 0 if empty
                entries[3].get() or "0",
                entries[4].get() or "0", 
                entries[5].get() or "0"
            )
            if success:
                if self.manager.save_students():
                    messagebox.showinfo("Success", message)
                    dialog.destroy()
                    self.view_all_students()
                else:
                    messagebox.showerror("Error","Failed to save file!")
            else:
                messagebox.showerror("Error", message)

        ctk.CTkButton(dialog, text="Add Student", command=submit).grid(row=6,column=0,columnspan=2,padx=12,pady=12, sticky="we")

    def update_student_dialog(self):
        code = simpledialog.askstring("Update Student","Enter Student Code:")
        if not code: return
        student = self.manager.get_student_by_code(code)
        if not student:
            messagebox.showerror("Not found","Student not found!")
            return

        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Update Student")
        dialog.geometry("380x340")
        dialog.transient(self.root)
        dialog.grab_set()

        labels = ["New Name","Course Mark 1","Course Mark 2","Course Mark 3","Exam Mark"]
        entries = []
        values = [student.name, student.mark1, student.mark2, student.mark3, student.exam_mark]
        for i,text in enumerate(labels):
            ctk.CTkLabel(dialog, text=text).grid(row=i,column=0,padx=12,pady=6, sticky="w")
            e = ctk.CTkEntry(dialog)
            e.insert(0,str(values[i]))
            e.grid(row=i,column=1,padx=12,pady=6)
            entries.append(e)

        def submit():
            success, message = self.manager.update_student(
                code,
                name=entries[0].get(),
                mark1=entries[1].get(),
                mark2=entries[2].get(),
                mark3=entries[3].get(),
                exam_mark=entries[4].get()
            )
            if success:
                if self.manager.save_students():
                    messagebox.showinfo("Success", message)
                    dialog.destroy()
                    self.view_all_students()
                else:
                    messagebox.showerror("Error","Failed to save file!")
            else:
                messagebox.showerror("Error", message)

        ctk.CTkButton(dialog, text="Update Student", command=submit).grid(row=5,column=0,columnspan=2,padx=12,pady=12, sticky="we")

    def delete_student(self):
        code = simpledialog.askstring("Delete Student","Enter Student Code:")
        if not code: return
        student = self.manager.get_student_by_code(code)
        if not student:
            messagebox.showerror("Not found","Student not found!")
            return
        confirm = messagebox.askyesno("Confirm", f"Delete {student.name}?")
        if confirm:
            success,message = self.manager.delete_student(code)
            if success:
                if self.manager.save_students():
                    messagebox.showinfo("Success", message)
                    self.view_all_students()
                else:
                    messagebox.showerror("Error","Failed to save file!")
            else:
                messagebox.showerror("Error", message)

    def sort_students(self):
        choice = simpledialog.askstring("Sort Students","Sort by:\n1-Name(A-Z)\n2-Name(Z-A)\n3-Percentage(High-Low)\n4-Percentage(Low-High)")
        students = self.manager.get_all_students()
        if not students: 
            messagebox.showinfo("Info","No students to sort.")
            return
            
        if choice=="1": 
            students.sort(key=lambda x:x.name)
            title="Sorted Name(A-Z)"
        elif choice=="2": 
            students.sort(key=lambda x:x.name, reverse=True)
            title="Sorted Name(Z-A)"
        elif choice=="3": 
            students.sort(key=lambda x:x.overall_percentage, reverse=True)
            title="Sorted % High-Low"
        elif choice=="4": 
            students.sort(key=lambda x:x.overall_percentage)
            title="Sorted % Low-High"
        else: 
            messagebox.showerror("Error","Invalid option!")
            return
            
        self.display_students_cards(students,title=title)

    # ---------------- Theme ----------------
    def change_theme(self,new_mode):
        ctk.set_appearance_mode(new_mode)

# -----------------------
# Main
# -----------------------
def main():
    root = ctk.CTk()
    app = StudentManagerApp(root)
    root.mainloop()

if __name__=="__main__":
    main()