"""
DATABASE.PY - SQLite Database Operations
=========================================
UNIT 5: SQLite database programming using DBAPI
         Simple ORM-like structure

This file contains:
1. Database connection and initialization
2. CRUD operations (Create, Read, Update, Delete)
3. Query methods
4. Database helper functions
"""

# Import required modules
import sqlite3                  # UNIT 5: SQLite database module (DBAPI)
import os
from datetime import datetime
from utils import (
    InvalidEmailError, 
    InvalidPhoneError,
    DuplicateStudentError,
    validate_email,
    validate_phone,
    validate_roll_number,
    is_valid_cgpa
)

# Database file path
DB_FILE = 'data/educonnect.db'


# ============================================================================
# UNIT 5: Database Connection Class (Simple ORM-like Structure)
# ============================================================================

class StudentDatabase:
    """
    UNIT 5: ORM-like class for managing student database operations
    This class encapsulates database functionality.
    
    Features:
    - Connection management
    - CRUD operations
    - Query methods
    """
    
    def __init__(self, db_file=DB_FILE):
        """
        Initialize database connection
        
        Parameters:
            db_file (str): Path to SQLite database file
        """
        self.db_file = db_file
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """
        UNIT 5: Establish database connection
        
        Returns:
            bool: True if connection successful
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
            
            # UNIT 5: sqlite3.connect() - Connect to SQLite database
            # check_same_thread=False allows use across multiple threads (GUI, web server, auto-save)
            self.connection = sqlite3.connect(self.db_file, check_same_thread=False)
            
            # Set row factory to return dictionaries instead of tuples
            self.connection.row_factory = sqlite3.Row
            
            # UNIT 5: Create cursor object
            self.cursor = self.connection.cursor()
            
            print(f"✓ Database connected: {self.db_file}")
            return True
            
        except sqlite3.Error as e:
            print(f"✗ Database connection error: {str(e)}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("✓ Database disconnected")
    
    # ====================================================================
    # DATABASE INITIALIZATION - Create tables
    # ====================================================================
    
    def create_tables(self):
        """
        UNIT 5: Create database tables for students and login
        Uses SQL CREATE TABLE statement
        """
        try:
            # Create STUDENTS table
            create_students_table = """
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                roll_no TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT NOT NULL,
                department TEXT NOT NULL,
                cgpa REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            # Create USERS table for login system
            create_users_table = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'admin',
                student_roll_no TEXT,
                FOREIGN KEY(student_roll_no) REFERENCES students(roll_no)
            )
            """
            
            # Create RESULTS table for student results
            create_results_table = """
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                roll_no TEXT NOT NULL,
                subject TEXT NOT NULL,
                marks REAL NOT NULL,
                FOREIGN KEY(roll_no) REFERENCES students(roll_no)
            )
            """
            
            # Execute all create table statements
            self.cursor.execute(create_students_table)
            self.cursor.execute(create_users_table)
            self.cursor.execute(create_results_table)
            
            # Commit changes to database
            self.connection.commit()
            print("✓ Database tables created successfully")
            
        except sqlite3.Error as e:
            print(f"✗ Error creating tables: {str(e)}")
    
    # ====================================================================
    # UNIT 5: CREATE OPERATION (INSERT)
    # ====================================================================
    
    def add_student(self, roll_no, name, email, phone, department, cgpa):
        """
        UNIT 5: Add a new student to database
        
        Parameters:
            roll_no, name, email, phone, department, cgpa: Student data
            
        Returns:
            int: Student ID if successful
            
        Raises:
            InvalidEmailError, InvalidPhoneError, DuplicateStudentError, ValueError
        """
        # Validate inputs using functions from utils
        validate_email(email)
        validate_phone(phone)
        validate_roll_number(roll_no)
        
        if not is_valid_cgpa(cgpa):
            raise ValueError("CGPA must be between 0 and 10")
        
        # Check if student already exists
        self.cursor.execute("SELECT * FROM students WHERE roll_no = ?", (roll_no,))
        if self.cursor.fetchone():
            raise DuplicateStudentError(f"Student with roll number {roll_no} already exists")
        
        try:
            # UNIT 5: SQL INSERT statement with parameterized query
            insert_query = """
            INSERT INTO students (roll_no, name, email, phone, department, cgpa)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            
            self.cursor.execute(insert_query, (roll_no, name, email, phone, department, cgpa))
            self.connection.commit()
            
            student_id = self.cursor.lastrowid
            print(f"✓ Student {name} added successfully (ID: {student_id})")
            return student_id
            
        except sqlite3.Error as e:
            print(f"✗ Database error: {str(e)}")
            raise ValueError(f"Database error: {str(e)}")
    
    # ====================================================================
    # UNIT 5: READ OPERATION (SELECT)
    # ====================================================================
    
    def get_all_students(self):
        """
        UNIT 5: Retrieve all students from database
        
        Returns:
            list: List of student dictionaries
        """
        try:
            # UNIT 5: SQL SELECT statement
            select_query = "SELECT * FROM students ORDER BY roll_no"
            self.cursor.execute(select_query)
            
            # Fetch all results and convert to list of dictionaries
            students = []
            for row in self.cursor.fetchall():
                students.append(dict(row))
            
            return students
            
        except sqlite3.Error as e:
            print(f"✗ Error retrieving students: {str(e)}")
            return []
    
    def get_student_by_roll_no(self, roll_no):
        """
        UNIT 5: Retrieve a specific student by roll number
        
        Parameters:
            roll_no (str): Student roll number
            
        Returns:
            dict: Student data or None if not found
        """
        try:
            # UNIT 5: SQL SELECT with WHERE clause
            select_query = "SELECT * FROM students WHERE roll_no = ?"
            self.cursor.execute(select_query, (roll_no,))
            
            row = self.cursor.fetchone()
            if row:
                return dict(row)
            return None
            
        except sqlite3.Error as e:
            print(f"✗ Error retrieving student: {str(e)}")
            return None
    
    def search_students(self, search_term):
        """
        UNIT 5: Search students by name or roll number
        
        Parameters:
            search_term (str): Search term
            
        Returns:
            list: List of matching students
        """
        try:
            # UNIT 5: SQL SELECT with LIKE operator for pattern matching
            search_query = """
            SELECT * FROM students 
            WHERE name LIKE ? OR roll_no LIKE ?
            ORDER BY name
            """
            
            search_pattern = f"%{search_term}%"
            self.cursor.execute(search_query, (search_pattern, search_pattern))
            
            students = [dict(row) for row in self.cursor.fetchall()]
            return students
            
        except sqlite3.Error as e:
            print(f"✗ Error searching students: {str(e)}")
            return []
    
    # ====================================================================
    # UNIT 5: UPDATE OPERATION
    # ====================================================================
    
    def update_student(self, roll_no, name=None, email=None, phone=None, 
                      department=None, cgpa=None):
        """
        UNIT 5: Update student information
        
        Parameters:
            roll_no (str): Student roll number
            name, email, phone, department, cgpa: Fields to update (optional)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Build update query dynamically based on provided parameters
            updates = []
            values = []
            
            if name is not None:
                updates.append("name = ?")
                values.append(name)
            if email is not None:
                validate_email(email)
                updates.append("email = ?")
                values.append(email)
            if phone is not None:
                validate_phone(phone)
                updates.append("phone = ?")
                values.append(phone)
            if department is not None:
                updates.append("department = ?")
                values.append(department)
            if cgpa is not None:
                if not is_valid_cgpa(cgpa):
                    raise ValueError("CGPA must be between 0 and 10")
                updates.append("cgpa = ?")
                values.append(cgpa)
            
            if not updates:
                print("✗ No fields to update")
                return False
            
            # Add roll_no to values for WHERE clause
            values.append(roll_no)
            
            # UNIT 5: SQL UPDATE statement
            update_query = f"UPDATE students SET {', '.join(updates)} WHERE roll_no = ?"
            
            self.cursor.execute(update_query, values)
            self.connection.commit()
            
            if self.cursor.rowcount > 0:
                print(f"✓ Student {roll_no} updated successfully")
                return True
            else:
                print(f"✗ Student {roll_no} not found")
                return False
                
        except (InvalidEmailError, InvalidPhoneError, ValueError) as e:
            print(f"✗ Validation error: {str(e)}")
            return False
        except sqlite3.Error as e:
            print(f"✗ Database error: {str(e)}")
            return False
    
    # ====================================================================
    # UNIT 5: DELETE OPERATION
    # ====================================================================
    
    def delete_student(self, roll_no):
        """
        UNIT 5: Delete a student from database
        
        Parameters:
            roll_no (str): Student roll number
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # UNIT 5: SQL DELETE statement
            delete_query = "DELETE FROM students WHERE roll_no = ?"
            self.cursor.execute(delete_query, (roll_no,))
            self.connection.commit()
            
            if self.cursor.rowcount > 0:
                print(f"✓ Student {roll_no} deleted successfully")
                return True
            else:
                print(f"✗ Student {roll_no} not found")
                return False
                
        except sqlite3.Error as e:
            print(f"✗ Error deleting student: {str(e)}")
            return False
    
    # ====================================================================
    # UTILITY METHODS
    # ====================================================================
    
    def get_student_count(self):
        """
        UNIT 5: Get total number of students
        
        Returns:
            int: Number of students in database
        """
        try:
            # UNIT 5: SQL COUNT function
            self.cursor.execute("SELECT COUNT(*) as count FROM students")
            result = self.cursor.fetchone()
            return result['count'] if result else 0
        except sqlite3.Error as e:
            print(f"✗ Error counting students: {str(e)}")
            return 0
    
    def get_statistics(self):
        """
        Get database statistics
        
        Returns:
            dict: Statistics including total students, departments, average CGPA
        """
        try:
            # Get total count
            self.cursor.execute("SELECT COUNT(*) as count FROM students")
            total = self.cursor.fetchone()['count']
            
            # Get average CGPA
            self.cursor.execute("SELECT AVG(cgpa) as avg_cgpa FROM students")
            avg_cgpa = self.cursor.fetchone()['avg_cgpa'] or 0
            
            # Get departments count
            self.cursor.execute("SELECT COUNT(DISTINCT department) as depts FROM students")
            departments = self.cursor.fetchone()['depts']
            
            return {
                'total_students': total,
                'average_cgpa': round(avg_cgpa, 2),
                'departments': departments
            }
        except sqlite3.Error as e:
            print(f"✗ Error getting statistics: {str(e)}")
            return {}
    
    # ====================================================================
    # USER/LOGIN METHODS
    # ====================================================================
    
    def add_user(self, username, password, role='admin', student_roll_no=None):
        """
        Add a new user for login system
        
        Parameters:
            username, password, role: User data
            student_roll_no: Optional roll number if role is 'student'
            
        Returns:
            bool: True if successful
        """
        try:
            insert_query = """
            INSERT INTO users (username, password, role, student_roll_no)
            VALUES (?, ?, ?, ?)
            """
            self.cursor.execute(insert_query, (username, password, role, student_roll_no))
            self.connection.commit()
            return True
        except sqlite3.Error:
            return False
    
    def verify_login(self, username, password):
        """
        Verify user login credentials
        
        Parameters:
            username, password: Login credentials
            
        Returns:
            dict: User data including role and student_roll_no if valid, None otherwise
        """
        try:
            query = "SELECT * FROM users WHERE username = ? AND password = ?"
            self.cursor.execute(query, (username, password))
            user = self.cursor.fetchone()
            if user:
                return dict(user)
            return None
        except sqlite3.Error:
            return None
    
    def get_user_by_username(self, username):
        """
        Get user by username
        
        Parameters:
            username (str): Username
            
        Returns:
            dict: User data or None if not found
        """
        try:
            query = "SELECT * FROM users WHERE username = ?"
            self.cursor.execute(query, (username,))
            user = self.cursor.fetchone()
            if user:
                return dict(user)
            return None
        except sqlite3.Error:
            return None
    
    # ====================================================================
    # RESULTS METHODS
    # ====================================================================
    
    def add_result(self, roll_no, subject, marks):
        """
        Add student result
        
        Parameters:
            roll_no, subject, marks: Result data
            
        Returns:
            bool: True if successful
        """
        try:
            insert_query = """
            INSERT INTO results (roll_no, subject, marks)
            VALUES (?, ?, ?)
            """
            self.cursor.execute(insert_query, (roll_no, subject, marks))
            self.connection.commit()
            return True
        except sqlite3.Error:
            return False
    
    def get_student_results(self, roll_no):
        """
        Get all results for a student
        
        Parameters:
            roll_no (str): Student roll number
            
        Returns:
            list: List of result records
        """
        try:
            query = "SELECT subject, marks FROM results WHERE roll_no = ?"
            self.cursor.execute(query, (roll_no,))
            results = [dict(row) for row in self.cursor.fetchall()]
            return results
        except sqlite3.Error:
            return []


# ============================================================================
# HELPER FUNCTION - Global database instance
# ============================================================================

# Create a global database instance
db = StudentDatabase()


def initialize_database():
    """
    Initialize database connection and create tables
    """
    db.connect()
    db.create_tables()
    return db
