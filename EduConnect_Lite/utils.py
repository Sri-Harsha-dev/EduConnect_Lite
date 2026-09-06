"""
UTILS.PY - Utility Functions and Helpers
=========================================
UNIT 2: File handling, Exceptions, Custom exceptions, Regex validation
UNIT 3: Regular Expressions

This file contains:
1. Custom Exceptions - For handling errors
2. Email & Phone Validation using Regular Expressions
3. File Export/Import Functions (CSV and JSON)
4. Helper Functions
"""

# Import required modules
import re                       # UNIT 3: Regular Expressions module
import json                     # For JSON file handling
import csv                      # For CSV file handling
from datetime import datetime   # For timestamps


# ============================================================================
# UNIT 2: CUSTOM EXCEPTIONS - Creating our own exception classes
# ============================================================================

class StudentError(Exception):
    """
    Base custom exception class for Student-related errors.
    This is a CUSTOM EXCEPTION that inherits from Exception.
    """
    pass


class InvalidEmailError(StudentError):
    """Custom exception when email is invalid."""
    pass


class InvalidPhoneError(StudentError):
    """Custom exception when phone number is invalid."""
    pass


class DuplicateStudentError(StudentError):
    """Custom exception when duplicate student is found."""
    pass


class FileOperationError(StudentError):
    """Custom exception for file handling errors."""
    pass


# ============================================================================
# UNIT 3: REGULAR EXPRESSIONS - Email and Phone Validation
# ============================================================================

def validate_email(email):
    """
    UNIT 3: Regular Expression validation for email
    
    Parameters:
        email (str): Email address to validate
        
    Returns:
        bool: True if valid, False otherwise
        
    Raises:
        InvalidEmailError: If email format is invalid
    """
    # Regular expression pattern for email validation
    # This checks for: characters@domain.extension
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, email):
        raise InvalidEmailError(f"Invalid email format: {email}")
    
    return True


def validate_phone(phone):
    """
    UNIT 3: Regular Expression validation for phone number
    
    Parameters:
        phone (str): Phone number to validate
        
    Returns:
        bool: True if valid, False otherwise
        
    Raises:
        InvalidPhoneError: If phone number is invalid
    """
    # Regular expression pattern for phone number
    # This accepts: 10 digits, optionally with +, -, or spaces
    phone_pattern = r'^[+]?[0-9\s\-()]{10,}$'
    
    if not re.match(phone_pattern, phone):
        raise InvalidPhoneError(f"Invalid phone format: {phone}")
    
    return True


def validate_roll_number(roll_no):
    """
    UNIT 3: Regular Expression validation for roll number
    
    Parameters:
        roll_no (str): Roll number to validate
        
    Returns:
        bool: True if valid, False otherwise
        
    Raises:
        ValueError: If roll number format is invalid
    """
    # Roll number pattern: 3 letters followed by 4 digits (e.g., CSE0001)
    roll_pattern = r'^[A-Z]{3}[0-9]{4}$'
    
    if not re.match(roll_pattern, roll_no):
        raise ValueError(f"Invalid roll number format: {roll_no}. Expected format: ABC1234 (3 letters + 4 digits)")
    
    return True


# ============================================================================
# UNIT 2: FILE HANDLING - Export and Import Functions
# ============================================================================

def export_to_csv(students, filename):
    """
    UNIT 2: File handling - Export student data to CSV file
    
    Parameters:
        students (list): List of student dictionaries
        filename (str): Path to save CSV file
        
    Raises:
        FileOperationError: If file writing fails
    """
    try:
        # Check if students list is empty
        if not students:
            raise FileOperationError("No students to export")
        
        # UNIT 2: open() function - Open file in write mode
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            # Get column names from first student
            fieldnames = ['Roll_No', 'Name', 'Email', 'Phone', 'Department', 'CGPA']
            
            # Create CSV writer object
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header row
            writer.writeheader()
            
            # Write each student's data
            # UNIT 1: List comprehension to filter and write students
            for student in students:
                writer.writerow(student)
        
        print(f"✓ CSV file exported successfully: {filename}")
        
    except IOError as e:
        raise FileOperationError(f"Failed to export CSV: {str(e)}")


def export_to_json(students, filename):
    """
    UNIT 2: File handling - Export student data to JSON file
    
    Parameters:
        students (list): List of student dictionaries
        filename (str): Path to save JSON file
        
    Raises:
        FileOperationError: If file writing fails
    """
    try:
        # Check if students list is empty
        if not students:
            raise FileOperationError("No students to export")
        
        # UNIT 2: open() function - Open file in write mode
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            # json.dump() - Write data to JSON file with nice formatting
            json.dump(students, jsonfile, indent=4, ensure_ascii=False)
        
        print(f"✓ JSON file exported successfully: {filename}")
        
    except IOError as e:
        raise FileOperationError(f"Failed to export JSON: {str(e)}")


def import_from_json(filename):
    """
    UNIT 2: File handling - Import student data from JSON file
    
    Parameters:
        filename (str): Path to JSON file
        
    Returns:
        list: List of student dictionaries
        
    Raises:
        FileOperationError: If file reading fails
    """
    try:
        # UNIT 2: open() function - Open file in read mode
        with open(filename, 'r', encoding='utf-8') as jsonfile:
            # json.load() - Read data from JSON file
            students = json.load(jsonfile)
        
        print(f"✓ Imported {len(students)} students from JSON")
        return students
        
    except FileNotFoundError:
        raise FileOperationError(f"File not found: {filename}")
    except json.JSONDecodeError:
        raise FileOperationError(f"Invalid JSON format in {filename}")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_current_timestamp():
    """
    Get current date and time as a formatted string.
    Used for logging and timestamping operations.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def is_valid_cgpa(cgpa):
    """
    UNIT 1: Validate CGPA (should be between 0 and 10)
    
    Parameters:
        cgpa (float): CGPA value
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        cgpa_float = float(cgpa)
        return 0 <= cgpa_float <= 10
    except (ValueError, TypeError):
        return False


def is_valid_name(name):
    """
    UNIT 1: Validate student name (only alphabets and spaces)
    
    Parameters:
        name (str): Student name
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Check if name contains only letters and spaces
    name_pattern = r'^[a-zA-Z\s]+$'
    return bool(re.match(name_pattern, name)) and len(name) > 0


# ============================================================================
# UNIT 1: GENERATORS - Generate sample data
# ============================================================================

def generate_sample_students():
    """
    UNIT 1: Generator function that yields sample student data
    Generators are functions that use 'yield' to produce values one at a time.
    
    Yields:
        dict: Student dictionary with sample data
    """
    # Sample student data
    sample_data = [
        {'Roll_No': 'CSE0001', 'Name': 'Raj Kumar', 'Email': 'raj.kumar@example.com', 
         'Phone': '9876543210', 'Department': 'CSE', 'CGPA': 8.5},
        {'Roll_No': 'CSE0002', 'Name': 'Priya Singh', 'Email': 'priya.singh@example.com', 
         'Phone': '9123456789', 'Department': 'CSE', 'CGPA': 9.2},
        {'Roll_No': 'ECE0001', 'Name': 'Amit Patel', 'Email': 'amit.patel@example.com', 
         'Phone': '9988776655', 'Department': 'ECE', 'CGPA': 7.8},
    ]
    
    # Yield each student one by one (this is a GENERATOR)
    for student in sample_data:
        yield student


def get_sample_students():
    """
    Convert generator output to list.
    Uses the generator function generate_sample_students().
    
    Returns:
        list: List of sample students
    """
    # UNIT 1: List comprehension with generator
    return list(generate_sample_students())


# ============================================================================
# UNIT 2: ASSERTIONS - Basic validation
# ============================================================================

def assert_valid_student_data(roll_no, name, email, phone, dept, cgpa):
    """
    UNIT 2: Assertions for basic data validation
    Assertions check conditions and raise AssertionError if false.
    
    Parameters:
        roll_no, name, email, phone, dept, cgpa: Student data
        
    Raises:
        AssertionError: If any validation fails
    """
    assert roll_no, "Roll number cannot be empty"
    assert name, "Name cannot be empty"
    assert email, "Email cannot be empty"
    assert phone, "Phone cannot be empty"
    assert dept, "Department cannot be empty"
    assert cgpa, "CGPA cannot be empty"


# ============================================================================
# UNIT 1: LIST COMPREHENSIONS
# ============================================================================

def get_students_by_department(students, department):
    """
    UNIT 1: List Comprehension to filter students by department
    
    Parameters:
        students (list): List of student dictionaries
        department (str): Department to filter by
        
    Returns:
        list: Filtered list of students
    """
    # This is a LIST COMPREHENSION - creates a new list by filtering
    return [student for student in students if student['Department'] == department]


def get_students_above_cgpa(students, min_cgpa):
    """
    UNIT 1: List Comprehension to filter students above certain CGPA
    
    Parameters:
        students (list): List of students
        min_cgpa (float): Minimum CGPA threshold
        
    Returns:
        list: Students with CGPA >= min_cgpa
    """
    # Another LIST COMPREHENSION example
    return [student for student in students if float(student['CGPA']) >= min_cgpa]


# ============================================================================
# UNIT 1: SORTING
# ============================================================================

def sort_students_by_cgpa(students, reverse=True):
    """
    UNIT 1: Sorting - Sort students by CGPA
    
    Parameters:
        students (list): List of students
        reverse (bool): If True, sort descending; else ascending
        
    Returns:
        list: Sorted list of students
    """
    # Sort using the sorted() function with key parameter
    return sorted(students, key=lambda student: float(student['CGPA']), reverse=reverse)


def sort_students_by_name(students):
    """
    UNIT 1: Sorting - Sort students by name alphabetically
    
    Parameters:
        students (list): List of students
        
    Returns:
        list: Sorted list of students by name
    """
    return sorted(students, key=lambda student: student['Name'])
