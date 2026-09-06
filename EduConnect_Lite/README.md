# EduConnect Lite - Student Management System

A **beginner-friendly** Python project that demonstrates a complete Student Management System with GUI, database, web portal, and file handling.

---

## 📋 Project Overview

**EduConnect Lite** is designed to teach **Python fundamentals** through a practical, real-world application. It includes:

- ✅ **Tkinter GUI** - Admin & Student Dashboards with dual-role login
- ✅ **Web Portal** - HTTP server with role-based student access
- ✅ **Dual Authentication** - Admin and Student login in GUI and web
- ✅ **SQLite Database** - Persistent data storage with user management
- ✅ **Input Validation** - Real-time email/phone validation with UI error messages
- ✅ **Session Management** - Secure cookie-based web sessions (1-hour timeout)
- ✅ **File Handling** - Export to CSV/JSON
- ✅ **Regular Expressions** - Email and phone pattern validation
- ✅ **Multithreading** - Auto-save and background web server
- ✅ **Command-line Interface** - CLI and CLI arguments
- ✅ **Exception Handling** - Robust error management

---

## 📂 Project Structure

```
EduConnect_Lite/
│
├── main.py              # Main entry point, Tkinter GUI, CLI handling
├── database.py          # SQLite database operations (CRUD)
├── utils.py            # Utilities, regex validation, file export/import
├── web_server.py       # Simple HTTP server for web portal
├── README.md           # This file
│
└── data/               # Data storage directory
    ├── educonnect.db   # SQLite database (created automatically)
    ├── auto_backup.json # Auto-save backup
    └── students_export.* # Exported files
```

---

## 🎓 Syllabus Topics Covered

### UNIT 1: Python Basics & Data Structures
✅ Objects and Classes  
✅ Numbers, Strings, Lists, Tuples, Dictionaries, Sets  
✅ Operators and Control Flow (if/else, loops)  
✅ Sorting and List Comprehensions  
✅ Generators and Iterators  

**Usage in Project:**
- `database.py`: Classes for ORM-like structure
- `utils.py`: Generators for sample data, list comprehensions for filtering
- `main.py`: Dictionaries for configuration, control flow in GUI

### UNIT 2: File Handling & Modules
✅ File I/O (open(), read, write)  
✅ File Methods and Attributes  
✅ Command-line Arguments (sys.argv, argparse)  
✅ File System Modules (os, pathlib)  
✅ Exceptions and Custom Exceptions  
✅ Modules and Packages  
✅ Namespaces and Importing  

**Usage in Project:**
- `utils.py`: CSV/JSON export using file handling
- `main.py`: argparse for CLI arguments
- `database.py`: os module for directory creation
- All files: Custom exceptions (InvalidEmailError, etc.)

### UNIT 3: Regular Expressions & Threading
✅ Regular Expressions (re module)  
✅ Email and Phone Pattern Matching  
✅ Threading and Multithreading  

**Usage in Project:**
- `utils.py`: Email validation with regex pattern
- `utils.py`: Phone number validation with regex
- `utils.py`: Roll number validation with regex
- `main.py`: Background threading for auto-save
- `web_server.py`: HTTP server running in thread

### UNIT 4: GUI & Web Programming
✅ Tkinter GUI Framework  
✅ Widgets and Layouts (Labels, Entry, Buttons, Listbox)  
✅ Event Handling and Callbacks  
✅ Simple Web Programming (http.server)  
✅ HTML Response Handling  

**Usage in Project:**
- `main.py`: Complete Tkinter GUI with login and dashboard
- `web_server.py`: HTTP server with custom request handlers
- `web_server.py`: HTML generation and serving

### UNIT 5: Database Programming
✅ SQLite Database (DBAPI)  
✅ Database Connection and Cursor  
✅ CRUD Operations (Create, Read, Update, Delete)  
✅ SQL Queries (SELECT, INSERT, UPDATE, DELETE)  
✅ Simple ORM-like Structure  

**Usage in Project:**
- `database.py`: Complete DBAPI implementation
- `database.py`: StudentDatabase class (ORM-like)
- `database.py`: All CRUD operations with SQL queries

---

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- No external dependencies (uses only Python standard library)

### Installation & Setup

**Step 1: Navigate to project directory**
```bash
cd EduConnect_Lite
```

**Step 2: Run the application**

#### Option A: GUI Mode (Default)
```bash
python main.py
```
or
```bash
python main.py --gui
```

**Admin Login Credentials:** 
- Username: `admin`
- Password: `admin123`

**Student Login Credentials (after running --add-sample):**
- Student 1: Username: `cse0001` | Password: `pass123`
- Student 2: Username: `cse0002` | Password: `pass123`
- Student 3: Username: `ece0001` | Password: `pass123`

#### Option B: Add Sample Data
```bash
python main.py --add-sample
```

#### Option C: Command-Line Interface
```bash
python main.py --cli
```

#### Option D: Web Server Only (With Student Access)
```bash
python main.py --web --port 8000
```
Then open browser: `http://localhost:8000`

**Web Portal Login:**
- Admin: admin / admin123 (Access all features)
- Student: cse0001 / pass123 (Access only own details)

#### Option E: Export to CSV/JSON
```bash
python main.py --add-sample --export csv
python main.py --add-sample --export json
```

---

## 📖 File Descriptions

### 1. `main.py` - Main Application Entry Point

**Topics Covered:**
- UNIT 1: Classes, dictionaries, control flow
- UNIT 2: argparse for CLI arguments
- UNIT 3: Threading for auto-save and web server
- UNIT 4: Tkinter GUI (LoginWindow, AdminDashboard, StudentDashboard)

**Key Features:**
- **Dual-role login system** - Admin and Student authentication
- **Admin dashboard** with student CRUD operations
- **Student dashboard** showing only own details and results
- **Input validation** with real-time error messages (email, phone)
- Search functionality
- Export to CSV/JSON
- Web portal integration
- CLI mode for headless operation
- Command-line argument parsing

**Important Classes & Functions:**
- `LoginWindow`: Tkinter login interface with role selection
- `AdminDashboard`: Admin GUI dashboard with CRUD operations
- `StudentDashboard`: Student GUI showing personal details only
- `add_student()`: Add new student with validation
- `delete_student()`: Remove student
- `update_student()`: Modify student info
- `validate_email()`: Real-time email validation
- `validate_phone()`: Real-time phone validation
- `auto_save_worker()`: Background thread for auto-save
- `cli_mode()`: Command-line interface
- `main()`: Entry point with argument handling

### 2. `database.py` - SQLite Database Management

**Topics Covered:**
- UNIT 5: SQLite DBAPI with user authentication
- UNIT 2: Exception handling, custom exceptions
- UNIT 1: Classes and ORM-like structure

**Key Features:**
- Database connection management
- Automatic table creation with user roles
- Complete CRUD operations for students
- Dual authentication system (Admin & Student users)
- Search functionality
- Statistics generation
- User/Login management with role-based access
- Results storage and retrieval
- Student roll number linking to user accounts

**Important Class:**
- `StudentDatabase`: ORM-like class with methods:
  - `add_student()`: INSERT new student
  - `get_all_students()`: SELECT all
  - `get_student_by_roll_no()`: SELECT by ID
  - `update_student()`: UPDATE student
  - `delete_student()`: DELETE student
  - `search_students()`: Pattern matching search
  - `get_statistics()`: Database statistics
  - `add_user()`: Add user with role (admin/student)
  - `verify_login()`: Authenticate user by role
  - `get_user_by_username()`: Retrieve user details

### 3. `utils.py` - Utilities and Helpers

**Topics Covered:**
- UNIT 3: Regular expressions
- UNIT 2: File handling, custom exceptions
- UNIT 1: Generators, list comprehensions, sorting

**Key Features:**
- Email validation with regex
- Phone number validation with regex
- Roll number validation
- CSV export functionality
- JSON export/import functionality
- Sample data generation (generator)
- Sorting by CGPA and name
- Custom exception classes

**Important Functions:**
- `validate_email()`: Regex validation
- `validate_phone()`: Phone pattern matching
- `export_to_csv()`: File export
- `export_to_json()`: JSON file handling
- `generate_sample_students()`: Generator function
- `get_students_by_department()`: List comprehension
- `sort_students_by_cgpa()`: Sorting with lambda

### 4. `web_server.py` - HTTP Web Server with Authentication

**Topics Covered:**
- UNIT 4: Web programming with http.server and sessions
- UNIT 3: Threading for background server
- UNIT 1: List comprehensions, string formatting, dictionaries for sessions

**Key Features:**
- Secure HTTP server with authentication
- Session management (1-hour timeout with MD5 hashing)
- Cookie-based authentication
- Role-based access control (Admin/Student)
- Custom request handlers with HTML generation
- Student dashboard (protected route)
- Admin features (protected routes)
- Public access pages
- 404 and access denied error handling

**Important Class:**
- `StudentRequestHandler`: Custom HTTP request handler with routes:
  - `GET  /`: Home page (role-based content)
  - `GET  /login`: Login form
  - `POST /login`: Login submission with authentication
  - `GET  /logout`: Logout and clear session
  - `GET  /students`: View all students (admin/public)
  - `GET  /student-results`: View individual results (admin)
  - `GET  /student-dashboard`: View own profile & results (students only)
  - `GET  /statistics`: Show database stats (admin/public)

**Session Management Functions:**
- `create_session()`: Create new session with MD5 hash ID
- `get_session()`: Retrieve valid session (with expiry check)
- `destroy_session()`: Remove session on logout
- `get_session_cookie()`: Extract session from request headers
- `set_session_cookie()`: Set session in response headers
- `get_nav_html()`: Generate role-based navigation bar

**Important Functions:**
- `start_web_server()`: Non-blocking server startup
- `start_web_server_blocking()`: Blocking mode for CLI

---

## 🎮 How to Use

### GUI Mode Tutorial

#### Admin Login
1. **Login as Admin**
   - Select "Admin" role (default)
   - Enter credentials: admin / admin123
   - Click "Login"
   - Admin dashboard opens with full functionality

#### Student Login
1. **Login as Student**
   - Select "Student" role
   - Enter credentials: cse0001 / pass123 (or other student)
   - Click "Login"
   - Student dashboard opens showing only own details
   - Can view personal information and results
   - Cannot access other students' data

#### Admin Operations

2. **Add Student**
   - Fill all form fields (Roll No, Name, Email, Phone, Department, CGPA)
   - **Validation automatically checks:**
     - Email format with helpful error message
     - Phone number (10+ digits) with format guidance
   - Click "Add Student"
   - Success message confirms addition

3. **View Students**
   - Students list auto-displays
   - Each entry shows: Roll No - Name (Department)

4. **Search**
   - Enter search term (name or roll number)
   - Click "Search"
   - View filtered results

5. **Update Student**
   - Select student from list
   - Click "Update"
   - Modify fields in popup dialog
   - Click "Save Changes"

6. **Delete Student**
   - Select student from list
   - Click "Delete"
   - Confirm deletion

7. **Export Data**
   - Go to File menu
   - Choose "Export to CSV" or "Export to JSON"
   - Select location to save file

8. **Web Portal**
   - Go to Tools → "View Web Portal"
   - Browser opens automatically
   - View all students and results

### CLI Mode Tutorial

```bash
python main.py --cli
```

Menu options:
- View all students
- Add new student
- Search students
- Export to CSV
- Export to JSON
- Show statistics
- Exit

### Web Server Access (With Role-Based Features)

**Start server:**
```bash
python main.py --web --port 8000
```

**Access in browser:**
```
http://localhost:8000
```

**Public Pages (without login):**
- `/` - Home page with navigation
- `/students` - All students list
- `/statistics` - Database statistics

**Admin Pages (after admin login):**
- `/students` - All students with details
- `/student-results` - Search results by roll number
- `/statistics` - Full analytics dashboard

**Student Pages (after student login):**
- `/student-dashboard` - View own profile and results (protected)
- Cannot access admin pages (shows "Access Denied")

**Authentication:**
- `/login` - Dual-role login form
- `/logout` - Clear session and logout

---

## 🔒 Dual Login System (Admin & Student)

The application includes a comprehensive role-based login system stored in the SQLite database.

**Default Admin Account:**
- Username: `admin`
- Password: `admin123`
- Role: Admin (access all features)

**Student Accounts (created with --add-sample):**
- Username: `cse0001` | Password: `pass123` | Roll: CSE0001
- Username: `cse0002` | Password: `pass123` | Roll: CSE0002
- Username: `ece0001` | Password: `pass123` | Roll: ECE0001
- Role: Student (access only own dashboard)

**Adding Users Programmatically:**
```python
# Add admin user
db.add_user('newadmin', 'password123', 'admin')

# Add student user linked to roll number
db.add_user('cse0003', 'pass123', 'student', student_roll_no='CSE0003')
```

**Features:**
- Role verification during login
- Session management with 1-hour timeout
- Secure cookie-based sessions (web portal)
- Access control based on role
- Student dashboard restricted to own data

---

## 📊 Database Schema

### Students Table
```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT NOT NULL,
    department TEXT NOT NULL,
    cgpa REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Users Table (with Role-Based Access)
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'admin',
    student_roll_no TEXT,
    FOREIGN KEY(student_roll_no) REFERENCES students(roll_no)
)
```

### Results Table
```sql
CREATE TABLE results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no TEXT NOT NULL,
    subject TEXT NOT NULL,
    marks REAL NOT NULL,
    FOREIGN KEY(roll_no) REFERENCES students(roll_no)
)
```

---

## 🔧 Validation Rules with UI Error Messages

### Email Validation (Regex)
- Pattern: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
- Example: `john.doe@example.com`
- **UI Error Message**: "Invalid email: Please enter a valid email address! Example: student@domain.com"

### Phone Validation (Regex)
- Pattern: `^[+]?[0-9\s\-()]{10,}$`
- Examples: `9876543210`, `+1-234-567-8900`, `(555) 123-4567`
- **UI Error Message**: "Invalid phone: Please enter a valid phone number! Expected: 10+ digits"
- **Validation Type**: Pre-submission check prevents database errors

### Roll Number Validation (Regex)
- Pattern: `^[A-Z]{3}[0-9]{4}$`
- Example: `CSE0001` (3 letters + 4 digits)

### CGPA Validation
- Range: 0.0 to 10.0

---

## 💾 Auto-Save Feature

The application supports background auto-saving:

**Enable Auto-Save:**
- GUI: Tools → Enable Auto-Save
- Default interval: 30 seconds

**Backup Location:**
- `data/auto_backup.json`

---

## 📤 Export Features

### CSV Export
- Format: Comma-separated values
- Includes: Roll No, Name, Email, Phone, Department, CGPA
- Location: User-selected

### JSON Export
- Format: Pretty-printed JSON
- Includes: Complete student records
- Location: User-selected

---

## 🐛 Sample Data

The project includes sample students:

| Roll No | Name | Email | Phone | Department | CGPA |
|---------|------|-------|-------|------------|------|
| CSE0001 | Raj Kumar | raj.kumar@example.com | 9876543210 | CSE | 8.5 |
| CSE0002 | Priya Singh | priya.singh@example.com | 9123456789 | CSE | 9.2 |
| ECE0001 | Amit Patel | amit.patel@example.com | 9988776655 | ECE | 7.8 |

**Add Sample Data:**
```bash
python main.py --add-sample
```

---

## ⚠️ Exception Handling

The project includes comprehensive exception handling:

### Custom Exceptions
- `StudentError`: Base exception
- `InvalidEmailError`: Invalid email format
- `InvalidPhoneError`: Invalid phone format
- `DuplicateStudentError`: Duplicate roll number
- `FileOperationError`: File I/O errors

### Error Handling
- Try-except blocks for all I/O operations
- User-friendly error messages in GUI
- Validation before database operations
- Assertion checks for data integrity

---

## 🎯 Key Learning Points

### For Beginners

1. **Object-Oriented Programming**
   - Create classes for database and GUI
   - Use inheritance and methods

2. **Data Structures**
   - Lists for student collections
   - Dictionaries for student records
   - Sets for unique values

3. **File Handling**
   - Read/write CSV files
   - Parse JSON data
   - Handle file operations safely

4. **Regular Expressions**
   - Pattern matching for validation
   - Email and phone verification

5. **GUI Development**
   - Build user interfaces with Tkinter
   - Handle events and callbacks
   - Dialog windows and message boxes

6. **Database Programming**
   - SQLite connection and queries
   - CRUD operations
   - Data persistence

7. **Threading**
   - Background operations
   - Non-blocking UI
   - Daemon threads

8. **Web Programming**
   - HTTP server basics
   - HTML generation
   - URL routing

---

## 📝 Code Comments

Every important section includes detailed comments explaining:
- What the code does
- Which syllabus unit it covers
- Parameters and return values
- Exception handling

---

## 🔍 Testing Suggestions

1. **Test Login**
   - Valid credentials
   - Invalid credentials
   - Empty fields

2. **Test CRUD**
   - Add students
   - Update information
   - Delete records
   - Search functionality

3. **Test Validation**
   - Invalid email
   - Invalid phone
   - Invalid CGPA
   - Duplicate roll numbers

4. **Test Export**
   - CSV export and import
   - JSON export and import
   - File location verification

5. **Test Web Portal**
   - View all students
   - View individual results
   - Statistics page
   - Navigation

6. **Test CLI**
   - All menu options
   - Data persistence
   - Export functionality

---

## ❌ Troubleshooting

### Issue: Database file not found
**Solution:** Run with `--add-sample` to create database
```bash
python main.py --add-sample
```

### Issue: Port 8000 already in use
**Solution:** Use different port
```bash
python main.py --web --port 8080
```

### Issue: GUI not displaying correctly
**Solution:** Ensure tkinter is installed
```bash
python -m tkinter
```

### Issue: File permission denied
**Solution:** Check file permissions or use different directory
```bash
# Make sure data directory exists
mkdir data
```

---

## 📚 Additional Resources

- Python Documentation: https://docs.python.org/3/
- Tkinter Tutorial: https://docs.python.org/3/library/tkinter.html
- SQLite Documentation: https://www.sqlite.org/docs.html
- Regular Expressions: https://docs.python.org/3/library/re.html
- HTTP Server: https://docs.python.org/3/library/http.server.html

---

## 📄 License

This project is created for educational purposes.

---

## 👨‍💻 Author Notes

**For Academic Presentations:**
- Clearly explain each module's purpose
- Demonstrate CRUD operations
- Show database schema
- Export and view exported files
- Explain validation logic
- Discuss threading benefits

**For Viva Questions:**
- Explain OOP concepts used
- Discuss database design
- Talk about regex patterns
- Explain GUI event handling
- Discuss threading implementation
- Explain error handling strategy

---

## ✨ Features Showcase

### What Makes This Project Great for Beginners:

✅ **Simple Architecture** - Only 4 main files  
✅ **No External Dependencies** - Uses only Python standard library  
✅ **Comprehensive Comments** - Every section explained  
✅ **Multiple Interfaces** - GUI, CLI, Web  
✅ **Real-World Application** - Practical use case  
✅ **Complete CRUD** - All database operations  
✅ **Error Handling** - Robust exception management  
✅ **Data Export** - CSV and JSON formats  
✅ **All Syllabus Topics** - Complete coverage  

---

## 🎉 Enjoy Learning!

This project is designed to help you master Python fundamentals through a practical, engaging application. Start small, experiment, and gradually understand how all the pieces fit together!

**Happy Coding! 🚀**
