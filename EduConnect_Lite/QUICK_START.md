# 🚀 Quick Start Guide - EduConnect Lite

## ⚡ Get Started in 5 Minutes

### Step 1: Check Python Installation
```bash
python --version
```
**Should be 3.7 or higher**

### Step 2: Navigate to Project
```bash
cd EduConnect_Lite
```

### Step 3: Run the Application (GUI Mode)
```bash
python main.py
```

### Step 4: Login as Admin
- Select "Admin" role (default)
- Username: `admin`
- Password: `admin123`
- Click "Login"

### Step 5: Add a Student
Fill the form fields:
- Roll No: `CSE0001`
- Name: `John Doe`
- Email: `john.doe@example.com`
- Phone: `9876543210`
- Department: `CSE`
- CGPA: `8.5`

Click "Add Student" ✓

---

## � Student Login (After Running --add-sample)

### Step 1: Start Application
```bash
python main.py
```

### Step 2: Select Student Role
- Click on "Student" radio button
- Username: `cse0001`
- Password: `pass123`
- Click "Login"

### Step 3: View Student Dashboard
- View your personal details (Name, Email, Phone, Department, CGPA)
- See your results (if available)
- Only your own data is visible
- Click "Logout" to exit

**Other Student Credentials:**
- `cse0002` / `pass123` - Priya Singh
- `ece0001` / `pass123` - Amit Patel

---

## 🌐 Web Portal with Dual Login

### Start Web Portal

### GUI Mode (Default)
```bash
python main.py
```

### Add Sample Data
```bash
python main.py --add-sample
```

### Command-Line Mode
```bash
python main.py --cli
```

### Web Server Only
```bash
python main.py --web --port 8000
```
Then open: `http://localhost:8000`

**Web Portal Login Credentials:**
- **Admin**: admin / admin123 (Access all features)
- **Student**: cse0001 / pass123 (View only own details)

### Export to CSV
```bash
python main.py --add-sample --export csv
```

### Export to JSON
```bash
python main.py --add-sample --export json
```

---

## 🎯 Basic Features

### Add Student
1. Fill all form fields
2. Click "Add Student"
3. See confirmation message

### View All Students
- Students automatically display in the list
- Shows: Roll No - Name (Department)

### Search Student
1. Enter search term in search box
2. Click "Search"
3. View filtered results

### Update Student
1. Click on a student in the list
2. Click "Update" button
3. Change fields in popup dialog
4. Click "Save Changes"

### Delete Student
1. Click on a student in the list
2. Click "Delete" button
3. Confirm deletion

### Export Data
1. Go to File menu
2. Choose "Export to CSV" or "Export to JSON"
3. Select where to save
4. File is saved

### View Web Portal
1. Go to Tools → "View Web Portal"
2. Browser opens automatically
3. Click on different pages

---

## ✅ Validation Rules

### Email
- Must have @ symbol and domain
- Example: `student@college.com`

### Phone
- At least 10 digits
- Can include +, -, (), and spaces
- Example: `9876543210` or `+1-234-567-8900`

### Roll Number
- 3 capital letters + 4 digits
- Example: `CSE0001`

### CGPA
- Between 0 and 10
- Example: `8.5`

---

## 🎓 Where to See Each Feature

| Feature | File | Covered Topic |
|---------|------|----------------|
| GUI | main.py | UNIT 4 - Tkinter |
| Database | database.py | UNIT 5 - SQLite |
| Validation | utils.py | UNIT 3 - Regex |
| File Export | utils.py | UNIT 2 - File Handling |
| Threading | main.py, web_server.py | UNIT 3 - Threading |
| Web Server | web_server.py | UNIT 4 - Web |
| CLI | main.py | UNIT 2 - Arguments |

---

## 📂 Files Explained

**main.py** → Main application, Tkinter GUI, CLI

**database.py** → SQLite database operations

**utils.py** → Validation, file export/import

**web_server.py** → Simple HTTP web server

**README.md** → Complete documentation

---

## 🔐 Default Login

```
Username: admin
Password: admin123
```

---

## 💡 Tips for Beginners

1. **Start with GUI mode** - Most visual way to learn
2. **Add sample data first** - Practice with real data
3. **Use search feature** - Try filtering students
4. **Export data** - Check the generated files
5. **Open web portal** - See the web interface
6. **Read code comments** - Every section is explained

---

## ❌ Common Issues

| Issue | Solution |
|-------|----------|
| "No module named tkinter" | tkinter comes with Python, ensure Python installation is correct |
| Port 8000 already in use | Use different port: `python main.py --web --port 8080` |
| Database not found | Run: `python main.py --add-sample` |
| Invalid email error | Check email format: `user@domain.com` |

---

## 🎉 Next Steps

After running the app:

1. **Explore the code** - Read the comments
2. **Modify the code** - Change colors, add fields
3. **Add new features** - Grades, attendance, etc.
4. **Study each unit** - Focus on one file at a time

---

## 📖 Learn More

See **README.md** for:
- Complete feature list
- Detailed file descriptions
- All validation rules
- Database schema
- Testing suggestions
- Academic presentation tips

---

## ✨ Happy Learning! 🚀

Remember: Start simple, experiment, and gradually understand the bigger picture!
