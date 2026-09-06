"""
Test script to verify add_student functionality
Tests: Database operations, validation, and error handling
"""

import sys
import os
import shutil

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import StudentDatabase
from utils import InvalidEmailError, InvalidPhoneError, DuplicateStudentError

def test_add_student():
    """Test adding a student with various scenarios"""
    
    # Clean up old data
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    if os.path.exists(data_dir):
        shutil.rmtree(data_dir)
    
    print("\n" + "="*60)
    print("TESTING ADD STUDENT FUNCTIONALITY")
    print("="*60)
    
    # Create fresh database
    db = StudentDatabase()
    db.connect()
    db.create_tables()
    
    # Test 1: Add valid student
    print("\n[Test 1] Adding valid student...")
    try:
        result = db.add_student(
            roll_no="CSE0001",
            name="John Doe",
            email="john@college.edu",
            phone="+91 9876543210",
            department="Computer Science",
            cgpa="8.5"
        )
        print(f"✓ Result: {result}")
        assert result is not None, "Should return student ID"
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test 2: Add another valid student
    print("\n[Test 2] Adding second valid student...")
    try:
        result = db.add_student(
            roll_no="CSE0002",
            name="Jane Smith",
            email="jane@college.edu",
            phone="9876543211",
            department="Computer Science",
            cgpa="9.0"
        )
        print(f"✓ Result: {result}")
        assert result is not None, "Should return student ID"
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test 3: Invalid email
    print("\n[Test 3] Adding student with invalid email...")
    try:
        result = db.add_student(
            roll_no="CSE0003",
            name="Bob Wilson",
            email="invalid-email",
            phone="9876543212",
            department="ECE",
            cgpa="7.5"
        )
        print(f"✗ Should have raised InvalidEmailError, but got: {result}")
    except InvalidEmailError as e:
        print(f"✓ Correctly caught InvalidEmailError: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
    
    # Test 4: Invalid phone
    print("\n[Test 4] Adding student with invalid phone...")
    try:
        result = db.add_student(
            roll_no="CSE0004",
            name="Alice Brown",
            email="alice@college.edu",
            phone="123",
            department="ECE",
            cgpa="7.5"
        )
        print(f"✗ Should have raised InvalidPhoneError, but got: {result}")
    except InvalidPhoneError as e:
        print(f"✓ Correctly caught InvalidPhoneError: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
    
    # Test 5: Invalid roll number format
    print("\n[Test 5] Adding student with invalid roll number format...")
    try:
        result = db.add_student(
            roll_no="INVALID",
            name="Charlie Davis",
            email="charlie@college.edu",
            phone="9876543213",
            department="ECE",
            cgpa="7.5"
        )
        print(f"✗ Should have raised error, but got: {result}")
    except Exception as e:
        print(f"✓ Correctly caught error: {e}")
    
    # Test 6: Duplicate roll number
    print("\n[Test 6] Adding student with duplicate roll number...")
    try:
        result = db.add_student(
            roll_no="CSE0001",
            name="Duplicate Name",
            email="duplicate@college.edu",
            phone="9876543214",
            department="ECE",
            cgpa="7.5"
        )
        print(f"✗ Should have raised DuplicateStudentError, but got: {result}")
    except DuplicateStudentError as e:
        print(f"✓ Correctly caught DuplicateStudentError: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
    
    # Test 7: Invalid CGPA
    print("\n[Test 7] Adding student with invalid CGPA...")
    try:
        result = db.add_student(
            roll_no="CSE0005",
            name="Eve Ford",
            email="eve@college.edu",
            phone="9876543215",
            department="ECE",
            cgpa="15.0"
        )
        print(f"✗ Should have raised error, but got: {result}")
    except ValueError as e:
        print(f"✓ Correctly caught ValueError: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
    
    # Test 8: View all students
    print("\n[Test 8] Retrieving all students...")
    students = db.get_all_students()
    print(f"✓ Found {len(students)} students in database")
    for student in students:
        print(f"  - {student['roll_no']}: {student['name']} ({student['email']})")
    
    # Clean up
    db.disconnect()
    print("\n" + "="*60)
    print("ALL TESTS COMPLETED")
    print("="*60 + "\n")

if __name__ == "__main__":
    test_add_student()
