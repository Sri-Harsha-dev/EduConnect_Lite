# 📦 Installation Guide

Complete installation instructions for EduConnect Lite on all platforms.

---

## ✅ Pre-requisites

- **Python 3.7 or higher**
- **pip** (usually comes with Python)
- **Git** (optional, for cloning repository)

---

## 🖥️ Installation Steps by Operating System

### Windows 10/11

#### Step 1: Install Python
1. Download Python from: https://www.python.org/downloads/
2. During installation, **CHECK** "Add Python to PATH"
3. Click "Install Now"

#### Step 2: Verify Installation
Open Command Prompt and type:
```bash
python --version
```

You should see: `Python 3.x.x`

#### Step 3: Navigate to Project
```bash
cd path\to\EduConnect_Lite
```

#### Step 4: Run Application
```bash
python main.py
```

**✓ Done! Application should launch**

---

### macOS

#### Step 1: Install Python
```bash
# Using Homebrew (recommended)
brew install python3
```

Or download from: https://www.python.org/downloads/

#### Step 2: Verify Installation
```bash
python3 --version
```

#### Step 3: Navigate to Project
```bash
cd path/to/EduConnect_Lite
```

#### Step 4: Run Application
```bash
python3 main.py
```

**✓ Done!**

---

### Linux (Ubuntu/Debian)

#### Step 1: Install Python
```bash
sudo apt update
sudo apt install python3 python3-pip
```

#### Step 2: Verify Installation
```bash
python3 --version
```

#### Step 3: Navigate to Project
```bash
cd path/to/EduConnect_Lite
```

#### Step 4: Run Application
```bash
python3 main.py
```

**✓ Done!**

---

## 🔍 Verify Installation

### Check Python Version
```bash
# Windows
python --version

# macOS/Linux
python3 --version
```

**Must be 3.7 or higher**

### Check pip Installation
```bash
# Windows
pip --version

# macOS/Linux
pip3 --version
```

### Verify tkinter (GUI Library)
```bash
# Windows & macOS
python -m tkinter

# Linux
python3 -m tkinter
```

A small window should appear. Close it to confirm.

---

## ⚠️ Troubleshooting

### Issue: "Python not found"
**Windows Solution:**
1. Go to Settings → System → About
2. Scroll down, click "Advanced system settings"
3. Click "Environment Variables"
4. Edit PATH and add: `C:\Users\YourUsername\AppData\Local\Programs\Python\Python39\`
5. Restart Command Prompt

**macOS/Linux Solution:**
```bash
# Check if installed
which python3
which python
```

### Issue: "No module named tkinter"

**Windows:**
```bash
# Tkinter comes with Python, reinstall:
python -m pip install --upgrade pip
```

**macOS:**
```bash
brew install python-tk
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt install python3-tk
```

**Linux (Fedora):**
```bash
sudo dnf install python3-tkinter
```

### Issue: Port 8000 Already in Use
Use a different port:
```bash
python main.py --web --port 8080
```

### Issue: Permission Denied (Linux/macOS)
```bash
chmod +x main.py
python3 main.py
```

---

## 📂 Project Structure Check

After installation, verify the structure:
```
EduConnect_Lite/
├── main.py              ✓
├── database.py          ✓
├── utils.py             ✓
├── web_server.py        ✓
├── README.md            ✓
├── QUICK_START.md       ✓
├── requirements.txt     ✓
├── .gitignore           ✓
└── data/                ✓ (created on first run)
```

---

## 🚀 First Run

### Run with Sample Data
```bash
python main.py --add-sample
```

This will:
- Create the SQLite database
- Add sample students
- Create admin user (admin/admin123)

### Launch GUI
```bash
python main.py
```

**Login with:**
- Username: `admin`
- Password: `admin123`

---

## 🌐 Virtual Environment (Optional)

For advanced users, isolate the project:

### Windows
```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Run application
python main.py
```

### macOS/Linux
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Run application
python3 main.py
```

---

## 📖 Next Steps

1. Read **QUICK_START.md** for 5-minute setup
2. Read **README.md** for complete documentation
3. Try running: `python main.py --add-sample`
4. Launch GUI: `python main.py`

---

## ✨ You're All Set!

The application should now be ready to use. Start learning Python with EduConnect Lite! 🎓

---

## 📞 Common Questions

**Q: Do I need to install packages with pip?**
A: No! This project uses only Python standard library.

**Q: Which Python version should I use?**
A: 3.7 or higher. 3.9+ is recommended.

**Q: Can I run on multiple computers?**
A: Yes! Just copy the folder to any computer with Python.

**Q: How do I update the code?**
A: Edit the .py files with any text editor. Python doesn't need compilation.

**Q: Can I modify the code?**
A: Yes! This is encouraged for learning. Make backups first.

---

## 🎓 Now Ready to Learn!

Happy coding! 🚀
