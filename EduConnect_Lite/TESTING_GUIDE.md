# 🧪 Testing Guide - EduConnect Lite

Complete testing checklist to verify all features work correctly.

---

## ✅ Pre-Testing Setup

### Step 1: Install Project
```bash
python main.py --add-sample
```

### Step 2: Launch Application
```bash
python main.py
```

---

## 🔐 Test 1: Login System

### Test Case 1.1: Valid Admin Login
**Steps:**
1. Launch application
2. Select "Admin" role (default)
3. Enter: Username: `admin`, Password: `admin123`
4. Click "Login"

**Expected Result:**
- ✅ Success message appears
- ✅ Login window closes
- ✅ Admin dashboard opens with full functionality

### Test Case 1.2: Valid Student Login
**Steps:**
1. Launch application (after running --add-sample)
2. Select "Student" role
3. Enter: Username: `cse0001`, Password: `pass123`
4. Click "Login"

**Expected Result:**
- ✅ Login successful
- ✅ Login window closes
- ✅ Student dashboard opens
- ✅ Shows only student's data (Raj Kumar, CSE0001)
- ✅ Cannot see other students' data

### Test Case 1.3: Invalid Username
**Steps:**
1. Select "Admin" role
2. Enter: Username: `wrong`, Password: `admin123`
3. Click "Login"

**Expected Result:**
- ❌ Error message: "Invalid credentials!"
- ✅ Login window remains open

### Test Case 1.4: Invalid Password
**Steps:**
1. Select "Admin" role
2. Enter: Username: `admin`, Password: `wrong`
3. Click "Login"

**Expected Result:**
- ❌ Error message: "Invalid credentials!"
- ✅ Login window remains open

### Test Case 1.5: Student Role Mismatch
**Steps:**
1. Select "Student" role
2. Enter: Username: `admin`, Password: `admin123`
3. Click "Login"

**Expected Result:**
- ❌ Error message: "Invalid credentials!" (role mismatch)
- ✅ Login window remains open

### Test Case 1.6: Empty Fields
**Steps:**
1. Leave fields empty
2. Click "Login"

**Expected Result:**
- ❌ Error message: "Please enter username and password"

---

## 👥 Test 2: Add Student (CRUD - Create)

### Test Case 2.1: Add Valid Student
**Steps:**
1. Fill form with:
   - Roll No: `CSE0005`
   - Name: `Alice Smith`
   - Email: `alice.smith@college.com`
   - Phone: `9876543215`
   - Department: `CSE`
   - CGPA: `8.7`
2. Click "Add Student"

**Expected Result:**
- ✅ Success message: "Student added successfully!"
- ✅ Student appears in listbox
- ✅ Form fields clear

### Test Case 2.2: Add with Invalid Email
**Steps:**
1. Fill form with invalid email: `invalid-email`
2. Click "Add Student"

**Expected Result:**
- ❌ Error message: "Invalid email: Please enter a valid email address! Example: student@domain.com"
- ✅ Student not added to database
- ✅ Form remains open for correction

### Test Case 2.3: Add with Invalid Phone
**Steps:**
1. Fill form with invalid phone: `123` (only 3 digits)
2. Click "Add Student"

**Expected Result:**
- ❌ Error message: "Invalid phone: Please enter a valid phone number! Expected: 10+ digits"
- ✅ Student not added to database
- ✅ Form remains open for correction

### Test Case 2.4: Add with Valid Phone Format Variations
**Steps:**
1. Test phone numbers:
   - `9876543210` (plain digits)
   - `+1-234-567-8900` (with country code and dash)
   - `(555) 123-4567` (with parentheses and spaces)
2. Add students with each phone format

**Expected Result:**
- ✅ All valid formats accepted
- ✅ Students added successfully

### Test Case 2.4: Add with Invalid CGPA
**Steps:**
1. Fill form with CGPA: `15` (> 10)
2. Click "Add Student"

**Expected Result:**
- ❌ Error message: "CGPA must be between 0 and 10"
- ✅ Student not added

### Test Case 2.5: Add with Empty Fields
**Steps:**
1. Leave one or more fields empty
2. Click "Add Student"

**Expected Result:**
- ❌ Error message: "Please fill all fields!"
- ✅ Student not added

### Test Case 2.6: Add Duplicate Roll Number
**Steps:**
1. Add student with Roll No: `CSE0001` (already exists)
2. Click "Add Student"

**Expected Result:**
- ❌ Error message: "Student with roll number CSE0001 already exists"
- ✅ Student not added

---

## 📋 Test 3: View Students (CRUD - Read)

### Test Case 3.1: View All Students
**Expected Result:**
- ✅ All students from database display in listbox
- ✅ Format: "Roll No - Name (Department)"

### Test Case 3.2: Student Count
**Steps:**
1. Add 5 students
2. Refresh list

**Expected Result:**
- ✅ Exactly 5 students shown in listbox

---

## 🔍 Test 4: Search Students

### Test Case 4.1: Search by Name
**Steps:**
1. Enter "Raj" in search box
2. Click "Search"

**Expected Result:**
- ✅ Only students with "Raj" in name appear
- ✅ Message shows: "Found X student(s)"

### Test Case 4.2: Search by Roll Number
**Steps:**
1. Enter "CSE" in search box
2. Click "Search"

**Expected Result:**
- ✅ Only students with "CSE" in roll number appear

### Test Case 4.3: Search with No Results
**Steps:**
1. Enter "XYZ123" in search box
2. Click "Search"

**Expected Result:**
- ✅ Message shows: "Found 0 student(s)"
- ✅ Listbox is empty

### Test Case 4.4: Refresh After Search
**Steps:**
1. Search for a student
2. Click "Refresh"

**Expected Result:**
- ✅ All students display again

---

## ✏️ Test 5: Update Student (CRUD - Update)

### Test Case 5.1: Update Student Name
**Steps:**
1. Select student from list
2. Click "Update"
3. Change name to "Updated Name"
4. Click "Save Changes"

**Expected Result:**
- ✅ Success message: "Student updated!"
- ✅ Name changed in listbox
- ✅ Database updated

### Test Case 5.2: Update Student Email
**Steps:**
1. Select student
2. Click "Update"
3. Change email to "newemail@college.com"
4. Click "Save Changes"

**Expected Result:**
- ✅ Email updated
- ✅ Database reflects change

### Test Case 5.3: Update with Invalid Email
**Steps:**
1. Select student
2. Click "Update"
3. Enter invalid email: `invalid`
4. Click "Save Changes"

**Expected Result:**
- ❌ Error message: "Invalid email format"
- ✅ Student not updated

### Test Case 5.4: Update Without Selection
**Steps:**
1. Click "Update" without selecting student

**Expected Result:**
- ⚠️ Warning message: "Please select a student!"

---

## 🗑️ Test 6: Delete Student (CRUD - Delete)

### Test Case 6.1: Delete with Confirmation
**Steps:**
1. Select student
2. Click "Delete"
3. Confirm deletion

**Expected Result:**
- ✅ Success message: "Student deleted!"
- ✅ Student removed from listbox
- ✅ Database updated

### Test Case 6.2: Delete Without Confirmation
**Steps:**
1. Select student
2. Click "Delete"
3. Click "No" on confirmation

**Expected Result:**
- ✅ Student not deleted
- ✅ Remains in listbox

### Test Case 6.3: Delete Without Selection
**Steps:**
1. Click "Delete" without selecting student

**Expected Result:**
- ⚠️ Warning message: "Please select a student!"

---

## 📊 Test 7: Export Functions

### Test Case 7.1: Export to CSV
**Steps:**
1. Go to File → "Export to CSV"
2. Choose location and filename
3. Click "Save"

**Expected Result:**
- ✅ Success message with filename
- ✅ CSV file created with all students
- ✅ File readable in text editor/Excel

### Test Case 7.2: Export to JSON
**Steps:**
1. Go to File → "Export to JSON"
2. Choose location and filename
3. Click "Save"

**Expected Result:**
- ✅ Success message with filename
- ✅ JSON file created
- ✅ File readable in text editor

### Test Case 7.3: Export with No Students
**Steps:**
1. Delete all students
2. Try to export

**Expected Result:**
- ⚠️ Warning message: "No students to export!"
- ✅ No file created

### Test Case 7.4: Verify Exported Data
**Steps:**
1. Export to CSV
2. Open CSV in text editor or Excel
3. Verify data accuracy

**Expected Result:**
- ✅ All columns present: Roll_No, Name, Email, Phone, Department, CGPA
- ✅ All student data correct
- ✅ Data matches database

---

## 👤 Test 8: Student Dashboard (GUI)

### Test Case 8.1: Student Dashboard Display
**Steps:**
1. Login as student: `cse0001` / `pass123`
2. Verify dashboard contents

**Expected Result:**
- ✅ Student dashboard opens
- ✅ Shows only student's data:
  - Roll Number: CSE0001
  - Name: Raj Kumar
  - Email: raj.kumar@example.com
  - Phone: 9876543210
  - Department: CSE
  - CGPA: 8.5
- ✅ Cannot see other students' information

### Test Case 8.2: Student Results Display
**Steps:**
1. Student dashboard open
2. Look at "My Results" section

**Expected Result:**
- ✅ Results table displays
- ✅ Shows subject and marks columns
- ✅ Displays "No results available" if no data

### Test Case 8.3: Student Logout
**Steps:**
1. Student dashboard open
2. Click "Logout" button

**Expected Result:**
- ✅ Returns to login screen
- ✅ Session cleared
- ✅ Cannot access dashboard without re-login

### Test Case 8.4: Refresh Button
**Steps:**
1. Student dashboard open
2. Click "Refresh" button

**Expected Result:**
- ✅ Dashboard updates with latest data
- ✅ No page reload, smooth refresh

---

## 🌐 Test 9: Web Portal with Authentication

### Test Case 9.1: Web Portal Login - Admin
**Steps:**
1. Start: `python main.py --web --port 8000`
2. Open: http://localhost:8000/login
3. Select "Admin" role
4. Enter: admin / admin123
5. Click "Login"

**Expected Result:**
- ✅ Login successful
- ✅ Redirected to home page
- ✅ Navigation bar shows: "Admin: admin"
- ✅ All admin links visible: Students, Statistics, Results

### Test Case 9.2: Web Portal Login - Student
**Steps:**
1. Open: http://localhost:8000/login
2. Select "Student" role
3. Enter: cse0001 / pass123
4. Click "Login"

**Expected Result:**
- ✅ Login successful
- ✅ Redirected to home page
- ✅ Navigation bar shows: "Student: cse0001"
- ✅ Only "My Details" link visible

### Test Case 9.3: Student Dashboard (Web)
**Steps:**
1. Login as student: cse0001 / pass123
2. Click "My Details" link

**Expected Result:**
- ✅ Student profile page displays
- ✅ Shows only own data (Raj Kumar, CSE0001)
- ✅ Personal details section visible
- ✅ Results section visible

### Test Case 9.4: Student Access Control
**Steps:**
1. Login as student
2. Try to access: http://localhost:8000/students

**Expected Result:**
- ✅ "Access Denied" message displays
- ✅ Helpful message: "Students cannot view all students"
- ✅ Link to "My Details" provided

### Test Case 9.5: Student Statistics Access Denied
**Steps:**
1. Login as student
2. Try to access: http://localhost:8000/statistics

**Expected Result:**
- ✅ Can still view public statistics (if public route)
- OR
- ✅ "Access Denied" message (if admin-only route)

### Test Case 9.6: Admin Web Portal Features
**Steps:**
1. Login as admin: admin / admin123
2. Access all pages:
   - /students
   - /student-results
   - /statistics

**Expected Result:**
- ✅ All pages accessible
- ✅ Admin can view all students
- ✅ Admin can search results
- ✅ Admin can view all statistics

### Test Case 9.7: Web Portal Logout
**Steps:**
1. Logged in as student or admin
2. Click "Logout" link

**Expected Result:**
- ✅ Redirected to login page
- ✅ Session cleared
- ✅ Cannot access protected pages without re-login

### Test Case 9.8: Session Persistence
**Steps:**
1. Login as student
2. Navigate: Home → My Details → Home
3. Check navbar

**Expected Result:**
- ✅ "Student: cse0001" remains in navbar
- ✅ Session persists across page navigation
- ✅ No re-login needed

### Test Case 9.9: Invalid Login
**Steps:**
1. Go to http://localhost:8000/login
2. Enter wrong credentials: admin / wrong
3. Click "Login"

**Expected Result:**
- ✅ Error handling (either error message or stay on login page)
- ✅ Not redirected to protected area

### Test Case 9.10: View All Students (Public)
**Steps:**
1. Without login, go to: http://localhost:8000/students

**Expected Result:**
- ✅ All students list displays (public access)
- ✅ OR shows "Public" version with limited info

---

## � Test 10: Auto-Save Feature

### Test Case 10.1: Enable Auto-Save
**Steps:**
1. Go to Tools → "Enable Auto-Save"

**Expected Result:**
- ✅ Auto-save enabled message
- ✅ Background process starts

### Test Case 10.2: Verify Auto-Save File
**Steps:**
1. Enable auto-save
2. Wait 30+ seconds
3. Check `data/auto_backup.json` file

**Expected Result:**
- ✅ Backup file created
- ✅ Contains current student data
- ✅ File is valid JSON

### Test Case 10.3: Disable Auto-Save
**Steps:**
1. Go to Tools → "Disable Auto-Save"

**Expected Result:**
- ✅ Auto-save disabled message
- ✅ No more backups created

---

## 📊 Test 11: Statistics

### Test Case 11.1: Show Statistics
**Steps:**
1. Go to Tools → "Show Statistics"

**Expected Result:**
- ✅ Dialog shows:
  - Total Students count
  - Average CGPA (calculated)
  - Number of departments

### Test Case 11.2: Verify Statistics Accuracy
**Steps:**
1. Add known students
2. View statistics

**Expected Result:**
- ✅ Statistics calculations correct
- ✅ Counts match actual data

---

## 💻 Test 12: CLI Mode

### Test Case 12.1: Launch CLI
**Steps:**
```bash
python main.py --cli
```

**Expected Result:**
- ✅ Menu displays in terminal
- ✅ 7 options shown

### Test Case 12.2: View All Students (CLI)
**Steps:**
1. Launch CLI
2. Choose option 1

**Expected Result:**
- ✅ Table displays in terminal
- ✅ All students shown

### Test Case 12.3: Add Student (CLI)
**Steps:**
1. Launch CLI
2. Choose option 2
3. Enter student details

**Expected Result:**
- ✅ Student added to database
- ✅ Success message shown

### Test Case 12.4: Search (CLI)
**Steps:**
1. Launch CLI
2. Choose option 3
3. Enter search term

**Expected Result:**
- ✅ Matching students found
- ✅ Count shown

### Test Case 12.5: Export (CLI)
**Steps:**
1. Launch CLI
2. Choose option 4 or 5

**Expected Result:**
- ✅ File exported
- ✅ Confirmation message

### Test Case 12.6: Statistics (CLI)
**Steps:**
1. Launch CLI
2. Choose option 6

**Expected Result:**
- ✅ Statistics displayed
- ✅ Data accurate

---

## 🌐 Test 13: Web Server (Standalone)

### Test Case 13.1: Launch Web Server
**Steps:**
```bash
python main.py --web
```

**Expected Result:**
- ✅ Server starts
- ✅ Message: "Web server running at: http://localhost:8000"

### Test Case 13.2: Access Web Server
**Steps:**
1. Start web server
2. Open browser
3. Navigate to: http://localhost:8000

**Expected Result:**
- ✅ Home page loads
- ✅ All links functional

### Test Case 13.3: Custom Port
**Steps:**
```bash
python main.py --web --port 8080
```

**Expected Result:**
- ✅ Server runs on port 8080
- ✅ Access via http://localhost:8080

---

## \ud83d\udd27 Test 13: Web Server (Standalone)

### Test Case 13.1: Launch Web Server
**Steps:**
```bash
python main.py --web
```

**Expected Result:**
- \u2705 Server starts
- \u2705 Message: "Web server running at: http://localhost:8000"

### Test Case 13.2: Access Web Server
**Steps:**
1. Start web server
2. Open browser
3. Navigate to: http://localhost:8000

**Expected Result:**
- \u2705 Home page loads
- \u2705 All links functional

### Test Case 13.3: Custom Port
**Steps:**
```bash
python main.py --web --port 8080
```

**Expected Result:**
- \u2705 Server runs on port 8080
- \u2705 Access via http://localhost:8080

---

## \ud83d\udd28 Test 14: Database

### Test Case 14.1: Database Creation
**Steps:**
1. Add student
2. Close application
3. Reopen application

**Expected Result:**
- ✅ Student still exists
- ✅ Data persisted in database

---

## ✔️ Test 15: Input Validation

### Test Case 15.1: Email Patterns
**Valid Emails to Test:**
- `user@domain.com` ✅
- `first.last@domain.co.uk` ✅
- `user+tag@domain.com` ✅

**Invalid Emails to Test:**
- `invalid@` ❌
- `@domain.com` ❌
- `user@.com` ❌

### Test Case 15.2: Phone Patterns
**Valid Phones to Test:**
- `9876543210` ✅
- `+1-234-567-8900` ✅
- `(555) 123-4567` ✅

**Invalid Phones to Test:**
- `123` ❌ (too short)

### Test Case 15.3: Roll Number Pattern
**Valid Roll Numbers to Test:**
- `CSE0001` ✅
- `ECE0050` ✅
- `BIT0999` ✅

**Invalid Roll Numbers to Test:**
- `cse0001` ❌ (lowercase)
- `CS0001` ❌ (only 2 letters)
- `CSE00010` ❌ (5 digits)

---

## 📝 Test 16: GUI Elements

### Test Case 16.1: Button Functionality
- ✅ All buttons respond to clicks
- ✅ No crashes
- ✅ Feedback messages appear

### Test Case 16.2: Text Entry
- ✅ Data entry works
- ✅ No characters lost
- ✅ Unicode supported

### Test Case 16.3: Listbox Scrolling
- ✅ Scrollbar works
- ✅ Can select items
- ✅ Multiple operations possible

### Test Case 16.4: Dialogs
- ✅ Dialog windows open correctly
- ✅ Forms submit properly
- ✅ Can cancel

---

## 🎯 Test Summary Checklist

```
Login System
  □ Valid credentials
  □ Invalid credentials
  □ Empty fields

CRUD Operations
  □ Add student
  □ View all students
  □ Search students
  □ Update student
  □ Delete student

Validation
  □ Email validation
  □ Phone validation
  □ CGPA validation
  □ Empty fields

Export
  □ Export to CSV
  □ Export to JSON
  □ Export with no data

Web Features
  □ Web portal launch
  □ View students page
  □ View results page
  □ Statistics page
  □ Navigation

Auto-Save
  □ Enable auto-save
  □ Disable auto-save
  □ Verify backup

CLI
  □ Launch CLI
  □ All menu options
  □ Data operations

Statistics
  □ Show statistics
  □ Verify calculations

Database
  □ Database creation
  □ Data persistence
  □ Multiple operations

GUI Elements
  □ All buttons work
  □ Text entry works
  □ Listbox functions
  □ Dialogs work
```

---

## 📊 Test Results Template

**Tester Name:** ________________  
**Date:** ________________  
**Python Version:** ________________  

| Test Case | Status | Notes |
|-----------|--------|-------|
| 1.1 | ✅/❌ | |
| 1.2 | ✅/❌ | |
| ... | ... | ... |

---

## 🐛 Issue Reporting

If you find a bug, document:
1. **Test Case:** Which test failed?
2. **Steps:** How to reproduce?
3. **Expected:** What should happen?
4. **Actual:** What actually happened?
5. **Error Message:** Any error shown?
6. **Python Version:** Which version?
7. **OS:** Windows/macOS/Linux?

---

## ✨ All Tests Passed?

**Congratulations!** 🎉

Your EduConnect Lite installation is working perfectly! You can now:
- ✅ Use the application
- ✅ Study the code
- ✅ Modify and extend it
- ✅ Present it academically
- ✅ Answer viva questions

Happy learning! 🚀
