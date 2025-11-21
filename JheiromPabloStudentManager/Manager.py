import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

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
                
                # Skip the first line (number of students)
                for line in lines[1:]:
                    data = line.strip().split(',')
                    if len(data) == 6:
                        student = Student(data[0], data[1], data[2], data[3], data[4], data[5])
                        self.students.append(student)
        except FileNotFoundError:
            messagebox.showerror("Error", f"File {self.filename} not found!")
    
    def save_students(self):
        """Save students to file"""
        try:
            with open(self.filename, 'w') as file:
                file.write(f"{len(self.students)}\n")
                for student in self.students:
                    file.write(student.to_file_string() + "\n")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")
            return False
    
    def get_all_students(self):
        """Return all students"""
        return self.students
    
    def get_student_by_code(self, code):
        """Get student by student code"""
        for student in self.students:
            if student.student_code == code:
                return student
        return None
    
    def get_student_by_name(self, name):
        """Get student by name (partial match)"""
        matches = []
        for student in self.students:
            if name.lower() in student.name.lower():
                matches.append(student)
        return matches
    
    def get_highest_scoring_student(self):
        """Get student with highest overall percentage"""
        if not self.students:
            return None
        return max(self.students, key=lambda x: x.overall_percentage)
    
    def get_lowest_scoring_student(self):
        """Get student with lowest overall percentage"""
        if not self.students:
            return None
        return min(self.students, key=lambda x: x.overall_percentage)
    
    def add_student(self, student_code, name, mark1, mark2, mark3, exam_mark):
        """Add a new student"""
        # Check if student code already exists
        if self.get_student_by_code(student_code):
            return False, "Student code already exists"
        
        try:
            student = Student(student_code, name, int(mark1), int(mark2), int(mark3), int(exam_mark))
            self.students.append(student)
            return True, "Student added successfully"
        except ValueError:
            return False, "Invalid marks entered"
    
    def delete_student(self, student_code):
        """Delete student by code"""
        student = self.get_student_by_code(student_code)
        if student:
            self.students.remove(student)
            return True, "Student deleted successfully"
        return False, "Student not found"
    
    def update_student(self, student_code, **kwargs):
        """Update student information"""
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

class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("800x600")
        
        self.manager = StudentManager()
        
        # Create menu
        self.create_menu()
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Text widget for displaying results
        self.text_output = tk.Text(self.main_frame, width=100, height=30, state=tk.DISABLED)
        self.text_output.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for text widget
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.text_output.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.text_output.configure(yscrollcommand=scrollbar.set)
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
    
    def create_menu(self):
        """Create the application menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Student Records menu
        records_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Student Records", menu=records_menu)
        records_menu.add_command(label="View All Students", command=self.view_all_students)
        records_menu.add_command(label="View Individual Student", command=self.view_individual_student)
        records_menu.add_separator()
        records_menu.add_command(label="Highest Scoring Student", command=self.show_highest_student)
        records_menu.add_command(label="Lowest Scoring Student", command=self.show_lowest_student)
        
        # Extended features menu
        extended_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Extended Features", menu=extended_menu)
        extended_menu.add_command(label="Sort Students", command=self.sort_students)
        extended_menu.add_command(label="Add Student", command=self.add_student)
        extended_menu.add_command(label="Delete Student", command=self.delete_student)
        extended_menu.add_command(label="Update Student", command=self.update_student)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Refresh Data", command=self.refresh_data)
        file_menu.add_command(label="Exit", command=self.root.quit)
    
    def refresh_data(self):
        """Refresh data from file"""
        self.manager.load_students()
        self.clear_output()
        self.display_text("Data refreshed from file.")
    
    def clear_output(self):
        """Clear the text output"""
        self.text_output.config(state=tk.NORMAL)
        self.text_output.delete(1.0, tk.END)
        self.text_output.config(state=tk.DISABLED)
    
    def display_text(self, text):
        """Display text in the output area"""
        self.text_output.config(state=tk.NORMAL)
        self.text_output.insert(tk.END, text + "\n")
        self.text_output.config(state=tk.DISABLED)
        self.text_output.see(tk.END)
    
    def format_student_output(self, student):
        """Format student information for display"""
        return (f"Name: {student.name}\n"
                f"Student Code: {student.student_code}\n"
                f"Total Coursework: {student.total_coursework}/60\n"
                f"Exam Mark: {student.exam_mark}/100\n"
                f"Overall Percentage: {student.overall_percentage:.2f}%\n"
                f"Grade: {student.grade}\n"
                f"{'-'*50}\n")
    
    def view_all_students(self):
        """Display all student records"""
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
        
        # Summary
        average_percentage = total_percentage / len(students)
        self.display_text(f"SUMMARY:")
        self.display_text(f"Number of students: {len(students)}")
        self.display_text(f"Average percentage: {average_percentage:.2f}%")
    
    def view_individual_student(self):
        """Display individual student record"""
        student_code = simpledialog.askstring("Find Student", "Enter Student Code:")
        if student_code:
            student = self.manager.get_student_by_code(student_code)
            if student:
                self.clear_output()
                self.display_text("INDIVIDUAL STUDENT RECORD")
                self.display_text("=" * 50)
                self.display_text(self.format_student_output(student))
            else:
                messagebox.showerror("Error", "Student not found!")
    
    def show_highest_student(self):
        """Display student with highest overall mark"""
        student = self.manager.get_highest_scoring_student()
        self.clear_output()
        if student:
            self.display_text("HIGHEST SCORING STUDENT")
            self.display_text("=" * 50)
            self.display_text(self.format_student_output(student))
        else:
            self.display_text("No students found.")
    
    def show_lowest_student(self):
        """Display student with lowest overall mark"""
        student = self.manager.get_lowest_scoring_student()
        self.clear_output()
        if student:
            self.display_text("LOWEST SCORING STUDENT")
            self.display_text("=" * 50)
            self.display_text(self.format_student_output(student))
        else:
            self.display_text("No students found.")
    
    def sort_students(self):
        """Sort students and display"""
        self.clear_output()
        students = self.manager.get_all_students()
        
        if not students:
            self.display_text("No students found.")
            return
        
        # Ask for sort order
        sort_order = simpledialog.askstring("Sort Students", 
                                           "Sort by:\n1 - Name (A-Z)\n2 - Name (Z-A)\n3 - Percentage (High-Low)\n4 - Percentage (Low-High)")
        
        if sort_order == '1':
            students.sort(key=lambda x: x.name)
            title = "STUDENTS SORTED BY NAME (A-Z)"
        elif sort_order == '2':
            students.sort(key=lambda x: x.name, reverse=True)
            title = "STUDENTS SORTED BY NAME (Z-A)"
        elif sort_order == '3':
            students.sort(key=lambda x: x.overall_percentage, reverse=True)
            title = "STUDENTS SORTED BY PERCENTAGE (HIGH-LOW)"
        elif sort_order == '4':
            students.sort(key=lambda x: x.overall_percentage)
            title = "STUDENTS SORTED BY PERCENTAGE (LOW-HIGH)"
        else:
            messagebox.showerror("Error", "Invalid sort option!")
            return
        
        self.display_text(title)
        self.display_text("=" * 50)
        
        for student in students:
            self.display_text(self.format_student_output(student))
    
    def add_student(self):
        """Add a new student"""
        # Create dialog window
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Student")
        dialog.geometry("300x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form fields
        ttk.Label(dialog, text="Student Code:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        code_entry = ttk.Entry(dialog)
        code_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        name_entry = ttk.Entry(dialog)
        name_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Course Mark 1 (0-20):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        mark1_entry = ttk.Entry(dialog)
        mark1_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Course Mark 2 (0-20):").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        mark2_entry = ttk.Entry(dialog)
        mark2_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Course Mark 3 (0-20):").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        mark3_entry = ttk.Entry(dialog)
        mark3_entry.grid(row=4, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Exam Mark (0-100):").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        exam_entry = ttk.Entry(dialog)
        exam_entry.grid(row=5, column=1, padx=5, pady=5)
        
        def submit():
            success, message = self.manager.add_student(
                code_entry.get(),
                name_entry.get(),
                mark1_entry.get(),
                mark2_entry.get(),
                mark3_entry.get(),
                exam_entry.get()
            )
            
            if success:
                if self.manager.save_students():
                    messagebox.showinfo("Success", message)
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to save to file!")
            else:
                messagebox.showerror("Error", message)
        
        ttk.Button(dialog, text="Add Student", command=submit).grid(row=6, column=0, columnspan=2, pady=10)
    
    def delete_student(self):
        """Delete a student"""
        student_code = simpledialog.askstring("Delete Student", "Enter Student Code to delete:")
        if student_code:
            student = self.manager.get_student_by_code(student_code)
            if student:
                confirm = messagebox.askyesno("Confirm Delete", 
                                            f"Are you sure you want to delete {student.name}?")
                if confirm:
                    success, message = self.manager.delete_student(student_code)
                    if success:
                        if self.manager.save_students():
                            messagebox.showinfo("Success", message)
                        else:
                            messagebox.showerror("Error", "Failed to save to file!")
                    else:
                        messagebox.showerror("Error", message)
            else:
                messagebox.showerror("Error", "Student not found!")
    
    def update_student(self):
        """Update a student's record"""
        student_code = simpledialog.askstring("Update Student", "Enter Student Code to update:")
        if student_code:
            student = self.manager.get_student_by_code(student_code)
            if student:
                # Create update dialog
                dialog = tk.Toplevel(self.root)
                dialog.title(f"Update Student: {student.name}")
                dialog.geometry("300x200")
                dialog.transient(self.root)
                dialog.grab_set()
                
                # Current values
                ttk.Label(dialog, text=f"Updating: {student.name}").grid(row=0, column=0, columnspan=2, pady=5)
                
                ttk.Label(dialog, text="New Name:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
                name_entry = ttk.Entry(dialog)
                name_entry.insert(0, student.name)
                name_entry.grid(row=1, column=1, padx=5, pady=5)
                
                ttk.Label(dialog, text="Course Mark 1:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
                mark1_entry = ttk.Entry(dialog)
                mark1_entry.insert(0, str(student.mark1))
                mark1_entry.grid(row=2, column=1, padx=5, pady=5)
                
                ttk.Label(dialog, text="Course Mark 2:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
                mark2_entry = ttk.Entry(dialog)
                mark2_entry.insert(0, str(student.mark2))
                mark2_entry.grid(row=3, column=1, padx=5, pady=5)
                
                ttk.Label(dialog, text="Course Mark 3:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
                mark3_entry = ttk.Entry(dialog)
                mark3_entry.insert(0, str(student.mark3))
                mark3_entry.grid(row=4, column=1, padx=5, pady=5)
                
                ttk.Label(dialog, text="Exam Mark:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
                exam_entry = ttk.Entry(dialog)
                exam_entry.insert(0, str(student.exam_mark))
                exam_entry.grid(row=5, column=1, padx=5, pady=5)
                
                def submit():
                    success, message = self.manager.update_student(
                        student_code,
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
                
                ttk.Button(dialog, text="Update Student", command=submit).grid(row=6, column=0, columnspan=2, pady=10)
            else:
                messagebox.showerror("Error", "Student not found!")

def main():
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()