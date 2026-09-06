#!/usr/bin/env python
"""Verify database contents"""

from database import db

db.connect()

print('=== USERS IN DATABASE ===')
print('Format: username / password (role) -> linked_student\n')
db.cursor.execute("SELECT * FROM users")
users = db.cursor.fetchall()
for user in users:
    u = dict(user)
    roll_no_str = f"Student: {u['student_roll_no']}" if u['student_roll_no'] else "Admin"
    print(f"  {u['username']} / {u['password']} ({u['role']}) -> {roll_no_str}")

print('\n=== STUDENTS IN DATABASE ===')
db.cursor.execute("SELECT roll_no, name, email, department, cgpa FROM students")
students = db.cursor.fetchall()
for student in students:
    s = dict(student)
    print(f"  {s['roll_no']} - {s['name']} ({s['department']}) - CGPA: {s['cgpa']}")

db.disconnect()

print('\n✓ Login Credentials:')
print('  ADMIN: admin / admin123')
print('  STUDENT 1: cse0001 / pass123 (Raj Kumar)')
print('  STUDENT 2: cse0002 / pass123 (Priya Singh)')
print('  STUDENT 3: ece0001 / pass123 (Amit Patel)')

