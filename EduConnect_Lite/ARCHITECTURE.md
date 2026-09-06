# 🏗️ Project Architecture & Structure

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    EduConnect Lite System                        │
└─────────────────────────────────────────────────────────────────┘

                    ┌──────────────────┐
                    │   User Interface │
                    └────────┬─────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
    ┌───▼────┐          ┌────▼────┐          ┌──▼───┐
    │  Tkinter GUI   │  Web Server    │  CLI Mode │
    │  (main.py)     │  (web_server.py)  │(main.py) │
    └────┬────┘      └────┬────┘      └──┬───┘
         │                │              │
         └────────────────┼──────────────┘
                          │
                 ┌────────▼────────┐
                 │  Database Layer │
                 │  (database.py)  │
                 └────────┬────────┘
                          │
                 ┌────────▼────────┐
                 │   SQLite DB      │
                 │ (educonnect.db)  │
                 └──────────────────┘

                 ┌─────────────────┐
                 │  Utilities      │
                 │  (utils.py)     │
                 │                 │
                 │ • Validation    │
                 │ • File Export   │
                 │ • Helpers       │
                 └─────────────────┘
```

---

## Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                        User Input                             │
│            (GUI, Web, CLI, Command-line)                     │
└────────────────┬─────────────────────────────────────────────┘
                 │
         ┌───────▼────────┐
         │  Validation    │
         │  (utils.py)    │
         │  • Email regex │
         │  • Phone regex │
         │  • CGPA check  │
         └───────┬────────┘
                 │
    ┌────────────▼────────────┐
    │   Database Operations   │
    │    (database.py)        │
    │                         │
    │ • INSERT (Add)          │
    │ • SELECT (View)         │
    │ • UPDATE (Modify)       │
    │ • DELETE (Remove)       │
    │ • SEARCH (Find)         │
    └────────────┬────────────┘
                 │
    ┌────────────▼────────────┐
    │     SQLite Database     │
    │    (educonnect.db)      │
    │                         │
    │ Tables:                 │
    │ • students              │
    │ • users                 │
    │ • results               │
    └────────────┬────────────┘
                 │
    ┌────────────▼─────────────┐
    │   File Export            │
    │   (utils.py)             │
    │                          │
    │ • CSV format             │
    │ • JSON format            │
    │ • Auto-backup            │
    └────────────┬──────────────┘
                 │
         ┌───────▼────────┐
         │   Output       │
         │   Files &      │
         │   Display      │
         └────────────────┘
```

---

## Module Dependency Graph

```
┌──────────────────────────────────────────────┐
│                   main.py                     │
│  (Tkinter GUI, CLI, Threading)               │
│                                              │
│  Imports:                                    │
│  ├─ database.py ──┐                         │
│  ├─ utils.py      ├─ All modules work       │
│  ├─ web_server.py─┤ together               │
│  └─ tkinter       │                        │
│     webbrowser    │                        │
│     argparse      │                        │
│     threading     │                        │
│     sys           │                        │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│               database.py                     │
│  (SQLite DBAPI, CRUD, ORM-like)             │
│                                              │
│  Imports:                                    │
│  ├─ sqlite3 (DBAPI)                         │
│  ├─ utils.py (validation, exceptions)       │
│  └─ Standard library modules                │
│     (os, datetime)                          │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│                utils.py                      │
│  (Validation, File I/O, Helpers)            │
│                                              │
│  Imports:                                    │
│  ├─ re (Regular Expressions)                │
│  ├─ json (JSON handling)                    │
│  ├─ csv (CSV handling)                      │
│  └─ Standard library modules                │
│     (datetime, etc)                         │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│               web_server.py                   │
│  (HTTP Server, HTML generation, Routing)     │
│                                              │
│  Imports:                                    │
│  ├─ http.server (Web server)                │
│  ├─ socketserver (TCP server)               │
│  ├─ database.py (Data access)               │
│  └─ Standard library modules                │
│     (urllib, threading, etc)                │
└──────────────────────────────────────────────┘
```

---

## File Organization & Relationships

```
EduConnect_Lite/
│
├── 🔧 CORE APPLICATION
│   │
│   ├─ main.py (630 lines)
│   │  ├─ LoginWindow class
│   │  ├─ AdminDashboard class
│   │  ├─ Auto-save threading
│   │  ├─ CLI mode
│   │  └─ Main entry point
│   │
│   ├─ database.py (470 lines)
│   │  ├─ StudentDatabase class
│   │  ├─ CRUD methods
│   │  ├─ Query methods
│   │  └─ Statistics
│   │
│   ├─ utils.py (380 lines)
│   │  ├─ Custom exceptions
│   │  ├─ Regex validators
│   │  ├─ File export/import
│   │  ├─ Generators
│   │  └─ Helper functions
│   │
│   └─ web_server.py (380 lines)
│      ├─ StudentRequestHandler class
│      ├─ HTML pages
│      ├─ Request routing
│      └─ Server startup
│
├── 📚 DOCUMENTATION
│   ├─ README.md (Complete guide)
│   ├─ QUICK_START.md (5-min setup)
│   ├─ INSTALLATION_GUIDE.md (OS-specific)
│   ├─ SYLLABUS_MAPPING.md (Topics → Code)
│   ├─ TESTING_GUIDE.md (Test cases)
│   ├─ PROJECT_SUMMARY.md (Overview)
│   └─ ARCHITECTURE.md (This file)
│
├── ⚙️ CONFIGURATION
│   ├─ requirements.txt (Dependencies)
│   └─ .gitignore (Git config)
│
└── 📁 DATA DIRECTORY (Auto-created)
    ├─ educonnect.db (SQLite database)
    ├─ auto_backup.json (Auto-save)
    ├─ students_export.csv (Exports)
    └─ students_export.json (Exports)
```

---

## Feature Implementation Map

```
┌─────────────────────────────────────────────────────┐
│                STUDENT MANAGEMENT FEATURES          │
└─────────────────────────────────────────────────────┘

ADD STUDENT
├─ GUI (main.py)
│  └─ Form → Validation (utils.py) → Database (database.py)
├─ CLI (main.py)
│  └─ Input → Validation (utils.py) → Database (database.py)
└─ File Import (utils.py)
   └─ JSON/CSV → Parse → Database (database.py)

VIEW STUDENTS
├─ GUI Listbox (main.py)
│  └─ Load from Database (database.py)
├─ Web Page (web_server.py)
│  └─ Generate HTML with data (database.py)
├─ CLI Table (main.py)
│  └─ Print formatted output (database.py)
└─ Search Filter (database.py)
   └─ Query by name/roll (database.py)

UPDATE STUDENT
├─ GUI Form (main.py)
│  └─ Validation (utils.py) → Update (database.py)
├─ CLI Input (main.py)
│  └─ Validation (utils.py) → Update (database.py)
└─ Web Form (web_server.py)
   └─ Submit → Update (database.py)

DELETE STUDENT
├─ GUI Confirmation (main.py)
│  └─ Delete (database.py)
├─ CLI Confirmation (main.py)
│  └─ Delete (database.py)
└─ Web Confirmation (web_server.py)
   └─ Delete (database.py)

EXPORT DATA
├─ CSV Export (utils.py)
│  └─ Database (database.py) → CSV file
├─ JSON Export (utils.py)
│  └─ Database (database.py) → JSON file
└─ Auto-backup (utils.py)
   └─ Threading (main.py) → JSON file

VALIDATION
├─ Email (utils.py)
│  └─ Regex pattern matching
├─ Phone (utils.py)
│  └─ Regex pattern matching
├─ Roll Number (utils.py)
│  └─ Format validation
└─ CGPA (utils.py)
   └─ Range validation (0-10)
```

---

## Database Schema & Relationships

```
┌─────────────────────────────┐
│      STUDENTS TABLE         │
├─────────────────────────────┤
│ id (PRIMARY KEY)            │
│ roll_no (UNIQUE)            │ ◄────┐
│ name                        │      │
│ email (UNIQUE)              │      │
│ phone                       │      │
│ department                  │      │
│ cgpa                        │      │
│ created_at                  │      │
└─────────────────────────────┘      │
                                     │
┌──────────────────────────────┐    │
│       RESULTS TABLE          │    │
├──────────────────────────────┤    │
│ id (PRIMARY KEY)             │    │
│ roll_no (FOREIGN KEY) ────────────┤
│ subject                      │    │
│ marks                        │    │
└──────────────────────────────┘    │
                                    │
┌──────────────────────────┐        │
│     USERS TABLE          │        │
├──────────────────────────┤        │
│ id (PRIMARY KEY)         │        │
│ username (UNIQUE)        │        │
│ password                 │        │
│ role                     │        │
└──────────────────────────┘        │
                           Login ───┘
```

---

## Threading Architecture

```
┌────────────────────────────────────────┐
│          Main Application              │
│      (GUI/CLI running on main thread)  │
└────────────────────┬───────────────────┘
                     │
           ┌─────────┴──────────┐
           │                    │
    ┌──────▼──────┐      ┌─────▼───────┐
    │  Web Server │      │ Auto-save   │
    │   Thread    │      │   Thread    │
    │  (Daemon)   │      │  (Daemon)   │
    │             │      │             │
    │ • Listen    │      │ • Wait 30s  │
    │   port 8000 │      │ • Export    │
    │ • Handle    │      │   students  │
    │   requests  │      │ • Backup    │
    │ • Generate  │      │   JSON file │
    │   HTML      │      │ • Repeat    │
    └─────────────┘      └─────────────┘
         │                      │
         └──────────────────────┘
              │
         ┌────▼─────────┐
         │  Database    │
         │  (SQLite)    │
         │              │
         │ • Thread-safe│
         │ • Handles    │
         │   concurrent │
         │   queries    │
         └──────────────┘
```

---

## Request Handling Flow

```
┌──────────────────────────────────────────────┐
│         User Action / Request                │
└────────────────┬─────────────────────────────┘
                 │
     ┌───────────▼───────────┐
     │   Route Handler       │
     │   (web_server.py or   │
     │    main.py)           │
     └───────────┬───────────┘
                 │
    ┌────────────▼─────────────┐
    │ Validate Input           │
    │ (utils.py)               │
    │ • Regex validation       │
    │ • Type checking          │
    │ • Range verification     │
    └────────────┬─────────────┘
                 │
    ┌────────────▼──────────────┐
    │ Database Operation        │
    │ (database.py)             │
    │ • Execute query           │
    │ • Handle transaction      │
    │ • Return result           │
    └────────────┬──────────────┘
                 │
    ┌────────────▼──────────────┐
    │ Format Response           │
    │                           │
    │ • HTML (Web)              │
    │ • JSON (API/File)         │
    │ • Table (CLI)             │
    │ • Message (GUI)           │
    └────────────┬──────────────┘
                 │
    ┌────────────▼──────────────┐
    │ Display to User           │
    │                           │
    │ • GUI window              │
    │ • Web browser             │
    │ • Terminal               │
    │ • Message box            │
    └───────────────────────────┘
```

---

## Code Execution Flow

```
START
  │
  ├─ main()
  │  │
  │  ├─ Parse command-line arguments (argparse)
  │  │
  │  ├─ Initialize database (database.py)
  │  │  ├─ Connect to SQLite
  │  │  └─ Create tables
  │  │
  │  ├─ Decision Point: Which mode?
  │  │  │
  │  │  ├─ GUI mode (DEFAULT)
  │  │  │  ├─ Create login window
  │  │  │  ├─ User enters credentials
  │  │  │  ├─ Verify with database
  │  │  │  ├─ Open admin dashboard
  │  │  │  └─ User interacts with GUI
  │  │  │
  │  │  ├─ CLI mode (--cli)
  │  │  │  ├─ Display menu
  │  │  │  ├─ Get user input
  │  │  │  ├─ Execute command
  │  │  │  └─ Repeat until exit
  │  │  │
  │  │  ├─ Web mode (--web)
  │  │  │  ├─ Start HTTP server
  │  │  │  ├─ Listen for requests
  │  │  │  ├─ Handle HTTP GET
  │  │  │  └─ Serve HTML pages
  │  │  │
  │  │  └─ Export mode (--export)
  │  │     ├─ Get all students
  │  │     ├─ Format (CSV/JSON)
  │  │     └─ Save to file
  │  │
  │  └─ Cleanup
  │     ├─ Close database
  │     ├─ Stop threads
  │     └─ Exit application
  │
END
```

---

## GUI Event Flow

```
┌──────────────────────────────┐
│   User Interaction (GUI)     │
│   • Button click             │
│   • Text entry               │
│   • Selection               │
│   • Menu action             │
└──────────────┬───────────────┘
               │
    ┌──────────▼──────────┐
    │ Event Handler       │
    │ (Callback function) │
    │ (main.py)           │
    └──────────┬──────────┘
               │
    ┌──────────▼───────────────┐
    │ Process Action           │
    │ • Get widget values      │
    │ • Validate input         │
    │ • Prepare parameters     │
    └──────────┬───────────────┘
               │
    ┌──────────▼────────────────┐
    │ Call Database/Util        │
    │ Function (database.py or  │
    │ utils.py)                 │
    └──────────┬────────────────┘
               │
    ┌──────────▼────────────────┐
    │ Handle Result             │
    │ • Success → Show message  │
    │ • Error → Show error      │
    │ • Refresh display         │
    └──────────┬────────────────┘
               │
    ┌──────────▼────────────────┐
    │ Update GUI                │
    │ • Refresh listbox         │
    │ • Clear form              │
    │ • Update labels           │
    └──────────────────────────┘
```

---

## Summary

This architecture demonstrates:

✅ **Modular Design** - Each file has specific responsibility  
✅ **Separation of Concerns** - GUI, DB, Utils are separate  
✅ **Data Flow** - Clear request → process → response cycle  
✅ **Scalability** - Easy to add new features  
✅ **Maintainability** - Code organized logically  
✅ **Threading** - Concurrent operations without blocking  
✅ **Database** - Persistent data with proper schema  
✅ **Multi-interface** - Same logic, different interfaces  

**Architecture is production-grade while remaining beginner-friendly!** 🎓
