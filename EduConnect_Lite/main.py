"""
MAIN.PY - Entry Point and Tkinter GUI
======================================
UNIT 1: Python basics, Objects and Classes, Control flow, Lists, Dictionaries
UNIT 2: Command-line arguments using sys.argv and argparse
UNIT 3: Threading and multithreading
UNIT 4: Tkinter GUI

This file contains:
1. Login System using Tkinter
2. Admin Dashboard with CRUD operations
3. Threading for background operations
4. Command-line argument handling
5. Auto-save functionality
"""

# Import required modules
import tkinter as tk                    # UNIT 4: Tkinter GUI module
from tkinter import messagebox, filedialog  # GUI message boxes and dialogs
import threading                        # UNIT 3: Threading module
import sys                              # For command-line arguments
import argparse                         # UNIT 2: Command-line argument parser
import webbrowser                       # To open web browser
import time                             # For sleep functionality
from database import initialize_database, db  # Database module
from utils import (                     # Utilities module
    export_to_csv, export_to_json, 
    validate_email, validate_phone,
    get_students_by_department,
    get_students_above_cgpa,
    sort_students_by_cgpa,
    InvalidEmailError, InvalidPhoneError, DuplicateStudentError
)
from web_server import start_web_server  # Web server module


# ============================================================================
# UNIT 1: GLOBAL VARIABLES AND CONFIGURATION
# ============================================================================

# Configuration dictionary (UNIT 1: Dictionaries)
config = {
    'web_server_running': False,
    'auto_save_enabled': False,
    'auto_save_interval': 30  # seconds
}

web_server_instance = None


# ============================================================================
# UNIT 3: THREADING - Auto-save functionality
# ============================================================================

def auto_save_worker():
    """
    UNIT 3: Background thread worker for auto-saving
    This runs continuously in a separate thread
    """
    while config['auto_save_enabled']:
        try:
            time.sleep(config['auto_save_interval'])
            
            if config['auto_save_enabled']:
                students = db.get_all_students()
                if students:
                    export_to_json(students, 'data/auto_backup.json')
                    print("✓ Auto-save completed")
                    
        except Exception as e:
            print(f"✗ Auto-save error: {str(e)}")


def start_auto_save():
    """Start auto-save in a background thread"""
    if not config['auto_save_enabled']:
        config['auto_save_enabled'] = True
        
        # UNIT 3: Create and start thread as daemon
        auto_save_thread = threading.Thread(target=auto_save_worker, daemon=True)
        auto_save_thread.start()
        
        print("✓ Auto-save enabled")


def stop_auto_save():
    """Stop auto-save"""
    config['auto_save_enabled'] = False
    print("✓ Auto-save disabled")


# ============================================================================
# UNIT 4: TKINTER GUI - Login Window
# ============================================================================

class LoginWindow:
    """
    UNIT 4: Tkinter Login Window with Admin and Student roles
    This is a CLASS (UNIT 1: Objects and classes)
    """
    
    def __init__(self, root):
        """
        Initialize login window
        
        Parameters:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("EduConnect Lite - Login")
        self.root.geometry("400x380")
        self.root.resizable(False, False)
        
        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (380 // 2)
        self.root.geometry(f"+{x}+{y}")
        
        # User role variable
        self.user_role = tk.StringVar(value="admin")
        
        # Create GUI elements
        self.create_widgets()
    
    def create_widgets(self):
        """Create login form widgets"""
        # Title label
        title = tk.Label(
            self.root, 
            text="EduConnect Lite", 
            font=("Arial", 18, "bold"),
            fg="#007bff"
        )
        title.pack(pady=20)
        
        # Subtitle
        subtitle = tk.Label(
            self.root,
            text="Student Management System",
            font=("Arial", 10),
            fg="#666"
        )
        subtitle.pack()
        
        # User role frame
        role_frame = tk.Frame(self.root)
        role_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(role_frame, text="Login as:", font=("Arial", 10)).pack(side="left")
        
        admin_radio = tk.Radiobutton(role_frame, text="Admin", variable=self.user_role, value="admin", font=("Arial", 10))
        admin_radio.pack(side="left", padx=(20, 10))
        
        student_radio = tk.Radiobutton(role_frame, text="Student", variable=self.user_role, value="student", font=("Arial", 10))
        student_radio.pack(side="left")
        
        # Username frame
        username_frame = tk.Frame(self.root)
        username_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(username_frame, text="Username:", font=("Arial", 10)).pack(side="left")
        self.username_entry = tk.Entry(username_frame, font=("Arial", 10))
        self.username_entry.pack(side="left", fill="x", expand=True, padx=(10, 0))
        
        # Password frame
        password_frame = tk.Frame(self.root)
        password_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(password_frame, text="Password:", font=("Arial", 10)).pack(side="left")
        self.password_entry = tk.Entry(password_frame, font=("Arial", 10), show="*")
        self.password_entry.pack(side="left", fill="x", expand=True, padx=(10, 0))
        
        # Login button
        login_btn = tk.Button(
            self.root,
            text="Login",
            font=("Arial", 10, "bold"),
            bg="#007bff",
            fg="white",
            command=self.verify_login
        )
        login_btn.pack(pady=20, padx=20, fill="x")
        
        # Demo credentials label
        demo_label = tk.Label(
            self.root,
            text="Demo: admin / admin123\nStudent: student1 / pass123",
            font=("Arial", 8),
            fg="#999"
        )
        demo_label.pack()
    
    def verify_login(self):
        """
        UNIT 2: Exception handling - Verify login credentials
        """
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.user_role.get()
        
        try:
            # Validate inputs
            if not username or not password:
                raise ValueError("Please enter username and password")
            
            # Verify credentials
            user = db.verify_login(username, password)
            
            if user:
                # Check if role matches
                if user['role'] == role:
                    messagebox.showinfo("Success", "Login successful!")
                    self.root.destroy()  # Close login window
                    
                    # Open appropriate dashboard
                    if role == "admin":
                        open_admin_dashboard()
                    else:
                        open_student_dashboard(username, user.get('student_roll_no'))
                else:
                    messagebox.showerror("Error", f"This account is for {user['role'].upper()}, not {role.upper()}!")
            else:
                messagebox.showerror("Error", "Invalid credentials!")
                
        except ValueError as e:
            messagebox.showerror("Error", str(e))


# ============================================================================
# UNIT 4: TKINTER GUI - Admin Dashboard
# ============================================================================

class AdminDashboard:
    """
    UNIT 4: Tkinter Admin Dashboard - Main application window
    """
    
    def __init__(self, root):
        """
        Initialize admin dashboard
        
        Parameters:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("EduConnect Lite - Admin Dashboard")
        self.root.geometry("900x700")
        
        # UNIT 1: Instance variables (class attributes)
        self.current_students = []
        self.selected_student_roll_no = tk.StringVar()
        
        self.create_menu()
        self.create_widgets()
        self.refresh_student_list()
    
    def create_menu(self):
        """Create menu bar with options"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export to CSV", command=self.export_csv)
        file_menu.add_command(label="Export to JSON", command=self.export_json)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="View Web Portal", command=self.open_web_portal)
        tools_menu.add_command(label="Enable Auto-Save", command=start_auto_save)
        tools_menu.add_command(label="Disable Auto-Save", command=stop_auto_save)
        tools_menu.add_separator()
        tools_menu.add_command(label="Show Statistics", command=self.show_statistics)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_widgets(self):
        """Create main dashboard widgets"""
        # ================== TOP FRAME - Add Student ===================
        top_frame = tk.LabelFrame(self.root, text="Add New Student", font=("Arial", 10, "bold"))
        top_frame.pack(pady=10, padx=10, fill="x")
        
        # UNIT 1: Form fields using grid layout
        tk.Label(top_frame, text="Roll No:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.roll_entry = tk.Entry(top_frame, width=15)
        self.roll_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(top_frame, text="Name:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.name_entry = tk.Entry(top_frame, width=15)
        self.name_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(top_frame, text="Email:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.email_entry = tk.Entry(top_frame, width=15)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(top_frame, text="Phone:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.phone_entry = tk.Entry(top_frame, width=15)
        self.phone_entry.grid(row=1, column=3, padx=5, pady=5)
        
        tk.Label(top_frame, text="Department:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.dept_entry = tk.Entry(top_frame, width=15)
        self.dept_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(top_frame, text="CGPA:").grid(row=2, column=2, sticky="w", padx=5, pady=5)
        self.cgpa_entry = tk.Entry(top_frame, width=15)
        self.cgpa_entry.grid(row=2, column=3, padx=5, pady=5)
        
        # Add button
        add_btn = tk.Button(
            top_frame,
            text="Add Student",
            font=("Arial", 10, "bold"),
            bg="#28a745",
            fg="white",
            command=self.add_student
        )
        add_btn.grid(row=3, column=0, columnspan=4, sticky="ew", padx=5, pady=10)
        
        # ================== MIDDLE FRAME - Student List ===================
        middle_frame = tk.LabelFrame(self.root, text="Student List", font=("Arial", 10, "bold"))
        middle_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Create listbox with scrollbar
        scrollbar = tk.Scrollbar(middle_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.student_listbox = tk.Listbox(
            middle_frame,
            yscrollcommand=scrollbar.set,
            font=("Arial", 9)
        )
        self.student_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.student_listbox.yview)
        
        # ================== BOTTOM FRAME - Actions ===================
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(pady=10, padx=10, fill="x")
        
        # Search frame
        search_frame = tk.Frame(bottom_frame)
        search_frame.pack(side="left", fill="x", expand=True)
        
        tk.Label(search_frame, text="Search:").pack(side="left", padx=(0, 5))
        self.search_entry = tk.Entry(search_frame, font=("Arial", 10))
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        search_btn = tk.Button(
            search_frame,
            text="Search",
            command=self.search_students,
            bg="#17a2b8",
            fg="white"
        )
        search_btn.pack(side="left", padx=2)
        
        refresh_btn = tk.Button(
            search_frame,
            text="Refresh",
            command=self.refresh_student_list,
            bg="#17a2b8",
            fg="white"
        )
        refresh_btn.pack(side="left", padx=2)
        
        # Action buttons frame
        action_frame = tk.Frame(bottom_frame)
        action_frame.pack(side="right", fill="x", padx=(10, 0))
        
        update_btn = tk.Button(
            action_frame,
            text="Update",
            command=self.update_student,
            bg="#ffc107",
            fg="black"
        )
        update_btn.pack(side="left", padx=2)
        
        delete_btn = tk.Button(
            action_frame,
            text="Delete",
            command=self.delete_student,
            bg="#dc3545",
            fg="white"
        )
        delete_btn.pack(side="left", padx=2)
    
    # ====================================================================
    # CRUD Operations
    # ====================================================================
    
    def add_student(self):
        """
        UNIT 1: Control flow - Add new student
        UNIT 2: Exception handling with enhanced validation
        """
        try:
            # Get form values
            roll_no = self.roll_entry.get().strip()
            name = self.name_entry.get().strip()
            email = self.email_entry.get().strip()
            phone = self.phone_entry.get().strip()
            department = self.dept_entry.get().strip()
            cgpa = self.cgpa_entry.get().strip()
            
            # Validate inputs
            if not all([roll_no, name, email, phone, department, cgpa]):
                messagebox.showerror("Error", "Please fill all fields!")
                return
            
            # Validate email format
            if not validate_email(email):
                messagebox.showerror("Email Error", "Please enter a valid email address!\nExample: student@domain.com")
                return
            
            # Validate phone format
            if not validate_phone(phone):
                messagebox.showerror("Phone Error", "Please enter a valid phone number!\nExpected: 10+ digits (can include +, -, spaces)")
                return
            
            # Add to database - exceptions will be raised here for other validations
            result = db.add_student(roll_no, name, email, phone, department, cgpa)
            
            # If we reach here, student was added successfully
            messagebox.showinfo("Success", "Student added successfully!")
            
            # Clear form fields
            self.clear_form()
            
            # Refresh student list
            self.refresh_student_list()
            
        except (InvalidEmailError, InvalidPhoneError) as e:
            # These should not occur now due to pre-validation, but keep for safety
            error_msg = str(e)
            if "email" in error_msg.lower():
                messagebox.showerror("Email Error", f"Invalid email: {error_msg}")
            else:
                messagebox.showerror("Phone Error", f"Invalid phone: {error_msg}")
        except (DuplicateStudentError, ValueError) as e:
            messagebox.showerror("Validation Error", str(e))
    
    def delete_student(self):
        """Delete selected student"""
        try:
            selection = self.student_listbox.curselection()
            
            if not selection:
                messagebox.showwarning("Warning", "Please select a student to delete!")
                return
            
            # Get roll number from listbox
            selected_text = self.student_listbox.get(selection[0])
            roll_no = selected_text.split(' - ')[0]
            
            # Confirm deletion
            if messagebox.askyesno("Confirm", f"Delete student {roll_no}?"):
                db.delete_student(roll_no)
                messagebox.showinfo("Success", "Student deleted!")
                self.refresh_student_list()
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def update_student(self):
        """
        Update selected student
        Opens a dialog for updating student information
        """
        try:
            selection = self.student_listbox.curselection()
            
            if not selection:
                messagebox.showwarning("Warning", "Please select a student!")
                return
            
            selected_text = self.student_listbox.get(selection[0])
            roll_no = selected_text.split(' - ')[0]
            
            # Get student details
            student = db.get_student_by_roll_no(roll_no)
            
            if not student:
                messagebox.showerror("Error", "Student not found!")
                return
            
            # Create update dialog
            self.open_update_dialog(student)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def open_update_dialog(self, student):
        """Open dialog for updating student"""
        # Create new window
        update_win = tk.Toplevel(self.root)
        update_win.title("Update Student")
        update_win.geometry("400x300")
        
        # Create entry fields with current values
        tk.Label(update_win, text="Roll No:").pack(pady=5)
        roll_label = tk.Label(update_win, text=student['roll_no'], font=("Arial", 10, "bold"))
        roll_label.pack()
        
        tk.Label(update_win, text="Name:").pack(pady=5)
        name_entry = tk.Entry(update_win, font=("Arial", 10))
        name_entry.insert(0, student['name'])
        name_entry.pack(padx=10, fill="x")
        
        tk.Label(update_win, text="Email:").pack(pady=5)
        email_entry = tk.Entry(update_win, font=("Arial", 10))
        email_entry.insert(0, student['email'])
        email_entry.pack(padx=10, fill="x")
        
        tk.Label(update_win, text="Phone:").pack(pady=5)
        phone_entry = tk.Entry(update_win, font=("Arial", 10))
        phone_entry.insert(0, student['phone'])
        phone_entry.pack(padx=10, fill="x")
        
        tk.Label(update_win, text="CGPA:").pack(pady=5)
        cgpa_entry = tk.Entry(update_win, font=("Arial", 10))
        cgpa_entry.insert(0, str(student['cgpa']))
        cgpa_entry.pack(padx=10, fill="x")
        
        def save_changes():
            """Save updated student information"""
            try:
                db.update_student(
                    student['roll_no'],
                    name=name_entry.get().strip(),
                    email=email_entry.get().strip(),
                    phone=phone_entry.get().strip(),
                    cgpa=cgpa_entry.get().strip()
                )
                messagebox.showinfo("Success", "Student updated!")
                update_win.destroy()
                self.refresh_student_list()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        save_btn = tk.Button(
            update_win,
            text="Save Changes",
            command=save_changes,
            bg="#28a745",
            fg="white"
        )
        save_btn.pack(pady=20, padx=10, fill="x")
    
    # ====================================================================
    # List Management
    # ====================================================================
    
    def refresh_student_list(self):
        """Refresh the student listbox"""
        # Get all students from database
        self.current_students = db.get_all_students()
        
        # Clear listbox
        self.student_listbox.delete(0, tk.END)
        
        # UNIT 1: List comprehension to format display
        # Add students to listbox
        for student in self.current_students:
            display_text = f"{student['roll_no']} - {student['name']} ({student['department']})"
            self.student_listbox.insert(tk.END, display_text)
    
    def search_students(self):
        """
        UNIT 1: Search students
        Uses search_students method from database
        """
        search_term = self.search_entry.get().strip()
        
        if not search_term:
            messagebox.showwarning("Warning", "Please enter search term!")
            return
        
        # Search in database
        results = db.search_students(search_term)
        
        # Clear and update listbox
        self.student_listbox.delete(0, tk.END)
        
        for student in results:
            display_text = f"{student['roll_no']} - {student['name']} ({student['department']})"
            self.student_listbox.insert(tk.END, display_text)
        
        messagebox.showinfo("Info", f"Found {len(results)} student(s)")
    
    def clear_form(self):
        """Clear all form fields"""
        # UNIT 1: Loop to clear all entry fields
        entries = [
            self.roll_entry, self.name_entry, self.email_entry,
            self.phone_entry, self.dept_entry, self.cgpa_entry
        ]
        
        for entry in entries:
            entry.delete(0, tk.END)
    
    # ====================================================================
    # Export/Import Functions
    # ====================================================================
    
    def export_csv(self):
        """Export students to CSV file"""
        try:
            students = db.get_all_students()
            
            if not students:
                messagebox.showwarning("Warning", "No students to export!")
                return
            
            # Ask for file location
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if filename:
                export_to_csv(students, filename)
                messagebox.showinfo("Success", f"Exported to {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def export_json(self):
        """Export students to JSON file"""
        try:
            students = db.get_all_students()
            
            if not students:
                messagebox.showwarning("Warning", "No students to export!")
                return
            
            # Ask for file location
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if filename:
                export_to_json(students, filename)
                messagebox.showinfo("Success", f"Exported to {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # ====================================================================
    # Additional Features
    # ====================================================================
    
    def open_web_portal(self):
        """Open web browser to view student results"""
        global web_server_instance
        
        try:
            if not web_server_instance:
                # Start web server in background thread
                web_server_instance = start_web_server('localhost', 8000)
            
            # Open browser
            webbrowser.open('http://localhost:8000')
            messagebox.showinfo("Info", "Web portal opened in browser")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open web portal: {str(e)}")
    
    def show_statistics(self):
        """Show database statistics"""
        try:
            stats = db.get_statistics()
            
            message = f"""
Database Statistics:

Total Students: {stats.get('total_students', 0)}
Average CGPA: {stats.get('average_cgpa', 0)}
Departments: {stats.get('departments', 0)}
            """
            
            messagebox.showinfo("Statistics", message)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
EduConnect Lite v1.0

A Simple Student Management System

Features:
• Add, Update, Delete Students
• View Student Records
• Export to CSV/JSON
• Web Portal for Results
• SQLite Database
• Auto-save Functionality

Powered by Python & Tkinter
        """
        messagebox.showinfo("About", about_text)


# ============================================================================
# UNIT 4: TKINTER GUI - Student Dashboard
# ============================================================================

class StudentDashboard:
    """
    UNIT 4: Tkinter Student Dashboard - Shows only student's own details
    """
    
    def __init__(self, root, username, roll_no):
        """
        Initialize student dashboard
        
        Parameters:
            root: Tkinter root window
            username: Student username
            roll_no: Student roll number
        """
        self.root = root
        self.root.title("EduConnect Lite - Student Portal")
        self.root.geometry("700x500")
        
        self.username = username
        self.roll_no = roll_no
        self.student_data = None
        
        self.create_widgets()
        self.load_student_data()
    
    def create_widgets(self):
        """Create student dashboard widgets"""
        # Title frame
        title_frame = tk.Frame(self.root, bg="#007bff", height=80)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        title = tk.Label(
            title_frame,
            text="Student Portal",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#007bff"
        )
        title.pack(pady=10)
        
        welcome = tk.Label(
            title_frame,
            text=f"Welcome, {self.username}",
            font=("Arial", 10),
            fg="white",
            bg="#007bff"
        )
        welcome.pack()
        
        # Content frame
        content_frame = tk.Frame(self.root)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Details label
        details_label = tk.Label(
            content_frame,
            text="Your Details:",
            font=("Arial", 12, "bold")
        )
        details_label.pack(anchor="w")
        
        # Text widget to display student details
        self.details_text = tk.Text(
            content_frame,
            font=("Arial", 10),
            height=15,
            width=60,
            state="disabled"
        )
        self.details_text.pack(fill="both", expand=True, pady=10)
        
        # Results section
        results_label = tk.Label(
            content_frame,
            text="Your Results:",
            font=("Arial", 12, "bold")
        )
        results_label.pack(anchor="w", pady=(10, 0))
        
        # Listbox for results
        self.results_listbox = tk.Listbox(
            content_frame,
            font=("Arial", 10),
            height=8
        )
        self.results_listbox.pack(fill="both", expand=True, pady=10)
        
        # Button frame
        button_frame = tk.Frame(content_frame)
        button_frame.pack(fill="x", pady=10)
        
        # Logout button
        logout_btn = tk.Button(
            button_frame,
            text="Logout",
            bg="#dc3545",
            fg="white",
            command=self.logout
        )
        logout_btn.pack(side="left", padx=5)
        
        # Refresh button
        refresh_btn = tk.Button(
            button_frame,
            text="Refresh",
            bg="#28a745",
            fg="white",
            command=self.load_student_data
        )
        refresh_btn.pack(side="left", padx=5)
    
    def load_student_data(self):
        """Load and display student data"""
        try:
            if not self.roll_no:
                messagebox.showerror("Error", "Student roll number not found!")
                return
            
            # Get student data
            student = db.get_student_by_roll_no(self.roll_no)
            
            if not student:
                messagebox.showerror("Error", "Student data not found!")
                return
            
            self.student_data = student
            
            # Display student details
            self.details_text.config(state="normal")
            self.details_text.delete(1.0, tk.END)
            
            details = f"""
Roll Number:      {student['roll_no']}
Name:             {student['name']}
Email:            {student['email']}
Phone:            {student['phone']}
Department:       {student['department']}
CGPA:             {student['cgpa']}
Created Date:     {student['created_at']}
            """
            
            self.details_text.insert(1.0, details)
            self.details_text.config(state="disabled")
            
            # Load results
            self.load_results()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {str(e)}")
    
    def load_results(self):
        """Load and display student results"""
        try:
            results = db.get_student_results(self.roll_no)
            
            self.results_listbox.delete(0, tk.END)
            
            if not results:
                self.results_listbox.insert(tk.END, "No results found")
            else:
                for result in results:
                    self.results_listbox.insert(
                        tk.END,
                        f"{result['subject']}: {result['marks']}/100"
                    )
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error loading results: {str(e)}")
    
    def logout(self):
        """Logout and return to login screen"""
        self.root.destroy()
        open_login_window()


# ============================================================================
# INITIALIZATION FUNCTIONS
# ============================================================================

def open_login_window():
    """Open login window"""
    login_root = tk.Tk()
    LoginWindow(login_root)
    login_root.mainloop()


def open_admin_dashboard():
    """Open admin dashboard"""
    admin_root = tk.Tk()
    AdminDashboard(admin_root)
    admin_root.mainloop()


def open_student_dashboard(username, roll_no):
    """Open student dashboard"""
    student_root = tk.Tk()
    StudentDashboard(student_root, username, roll_no)
    student_root.mainloop()


# ============================================================================
# UNIT 2: COMMAND-LINE ARGUMENTS HANDLING
# ============================================================================

def setup_cli_arguments():
    """
    UNIT 2: Command-line arguments using argparse
    
    Allows running the program with different options from command line
    """
    parser = argparse.ArgumentParser(
        description="EduConnect Lite - Student Management System",
        epilog="Example: python main.py --gui"
    )
    
    # GUI option
    parser.add_argument(
        '--gui',
        action='store_true',
        help='Launch GUI application (default)'
    )
    
    # CLI mode
    parser.add_argument(
        '--cli',
        action='store_true',
        help='Run in command-line mode'
    )
    
    # Web server only
    parser.add_argument(
        '--web',
        action='store_true',
        help='Start only web server'
    )
    
    # Port for web server
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='Web server port (default: 8000)'
    )
    
    # Add sample data
    parser.add_argument(
        '--add-sample',
        action='store_true',
        help='Add sample student data to database'
    )
    
    # Export option
    parser.add_argument(
        '--export',
        choices=['csv', 'json'],
        help='Export students to CSV or JSON'
    )
    
    return parser.parse_args()


def add_sample_data():
    """Add sample student data to database with student login accounts"""
    from utils import get_sample_students
    
    print("Adding sample data...")
    
    for student in get_sample_students():
        try:
            db.add_student(
                student['Roll_No'],
                student['Name'],
                student['Email'],
                student['Phone'],
                student['Department'],
                student['CGPA']
            )
            print(f"✓ Student {student['Name']} added successfully")
            
        except DuplicateStudentError:
            # Student already exists, continue to create user account
            print(f"  Student {student['Roll_No']} already exists, skipping...")
        except Exception as e:
            print(f"✗ Error adding student {student['Roll_No']}: {str(e)}")
            continue
        
        # Create student login account using roll_no as username
        try:
            student_username = student['Roll_No'].lower()
            student_password = "pass123"  # Default password for sample students
            
            # Check if user already exists
            existing_user = db.get_user_by_username(student_username)
            if existing_user:
                print(f"  Login account for {student_username} already exists")
            else:
                # Add user account for this student
                if db.add_user(student_username, student_password, role='student', student_roll_no=student['Roll_No']):
                    print(f"✓ Login account created: {student_username} / {student_password}")
                else:
                    print(f"✗ Failed to create login account for {student_username}")
        except Exception as e:
            print(f"✗ Error creating login account: {str(e)}")
    
    print("✓ Sample data initialization complete")


def cli_mode():
    """
    UNIT 2: CLI mode - Command-line interface
    Simple menu-driven interface for command line
    """
    print("\n" + "="*50)
    print("EduConnect Lite - CLI Mode")
    print("="*50 + "\n")
    
    while True:
        print("\nMenu:")
        print("1. View all students")
        print("2. Add student")
        print("3. Search student")
        print("4. Export to CSV")
        print("5. Export to JSON")
        print("6. Show statistics")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        try:
            if choice == '1':
                students = db.get_all_students()
                if not students:
                    print("No students found")
                else:
                    print(f"\n{'Roll No':<10} {'Name':<15} {'Department':<10} {'CGPA':<6}")
                    print("-" * 45)
                    for s in students:
                        print(f"{s['roll_no']:<10} {s['name']:<15} {s['department']:<10} {s['cgpa']:<6}")
            
            elif choice == '2':
                roll = input("Roll Number: ").strip()
                name = input("Name: ").strip()
                email = input("Email: ").strip()
                phone = input("Phone: ").strip()
                dept = input("Department: ").strip()
                cgpa = input("CGPA: ").strip()
                
                db.add_student(roll, name, email, phone, dept, cgpa)
            
            elif choice == '3':
                search_term = input("Search term: ").strip()
                results = db.search_students(search_term)
                if results:
                    print(f"\nFound {len(results)} student(s):")
                    for s in results:
                        print(f"  {s['roll_no']} - {s['name']}")
                else:
                    print("No students found")
            
            elif choice == '4':
                students = db.get_all_students()
                if students:
                    export_to_csv(students, 'data/students_export.csv')
            
            elif choice == '5':
                students = db.get_all_students()
                if students:
                    export_to_json(students, 'data/students_export.json')
            
            elif choice == '6':
                stats = db.get_statistics()
                print(f"\nTotal Students: {stats.get('total_students', 0)}")
                print(f"Average CGPA: {stats.get('average_cgpa', 0)}")
                print(f"Departments: {stats.get('departments', 0)}")
            
            elif choice == '7':
                print("Exiting...")
                break
            
            else:
                print("Invalid choice!")
                
        except Exception as e:
            print(f"Error: {str(e)}")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """
    UNIT 2: Main entry point with command-line argument handling
    """
    # Parse command-line arguments
    args = setup_cli_arguments()
    
    # Initialize database
    print("Initializing database...")
    initialize_database()
    
    # Add default admin user if database is empty
    try:
        user = db.verify_login('admin', 'admin123')
        if not user:
            db.add_user('admin', 'admin123', 'admin')
            print("✓ Admin user created (admin / admin123)")
    except Exception:
        pass
    
    # Handle sample data option
    if args.add_sample:
        add_sample_data()
    
    # Handle export option
    if args.export:
        students = db.get_all_students()
        if args.export == 'csv':
            export_to_csv(students, 'data/students_export.csv')
        elif args.export == 'json':
            export_to_json(students, 'data/students_export.json')
        return
    
    # Handle web-only mode
    if args.web:
        from web_server import start_web_server_blocking
        start_web_server_blocking('localhost', args.port)
        return
    
    # Handle CLI mode
    if args.cli:
        cli_mode()
        return
    
    # Default: Launch GUI
    print("✓ Launching GUI...")
    open_login_window()
    
    # Clean up
    db.disconnect()


# ============================================================================
# UNIT 2: Script Entry Point using if __name__ == '__main__'
# ============================================================================

if __name__ == '__main__':
    """
    UNIT 2: This ensures the script runs only when executed directly,
    not when imported as a module
    """
    main()
