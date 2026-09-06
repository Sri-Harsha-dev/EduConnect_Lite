# EduConnect Lite - Web Portal Student Login

## Features

### Web Portal Updates
The web portal now includes complete authentication and role-based access control:

#### **Login System**
- **Unified Login Page** (`/login`) for both Admin and Student
- **Session Management** using secure cookies (1-hour timeout)
- **Role-based Access Control** - Different features for Admin vs Students

#### **Admin Features** (after login)
- View all students
- View student results  
- View statistics and analytics
- Access to all portal features

#### **Student Features** (after login)
- **My Details** (`/student-dashboard`) - View own profile and results only
- Students cannot access other students' data
- Secure, personalized portal experience
- Logout functionality

#### **Public Access** (without login)
- Home page with navigation
- View all students (public list)
- View statistics (public overview)

#### **Routes**
```
GET  /               - Home page
GET  /login          - Login form
POST /login          - Login submission
GET  /logout         - Logout and clear session
GET  /students       - View all students (public or admin)
GET  /student-results - View student results by roll number (admin)
GET  /student-dashboard - View own details and results (students only)
GET  /statistics     - View system statistics (public or admin)
```

## Testing the Web Portal

### 1. Start the Web Portal
```bash
python main.py --web
# Or run the GUI and click "View Web Portal"
```

### 2. Access in Browser
Navigate to: `http://localhost:8000`

### 3. Test Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**Student Accounts:**
- Username: `cse0001`, Password: `pass123` (Raj Kumar)
- Username: `cse0002`, Password: `pass123` (Priya Singh)
- Username: `ece0001`, Password: `pass123` (Amit Patel)

### 4. Test Scenarios

#### Admin Login:
1. Click "Login" button
2. Select "Admin" role
3. Enter: admin / admin123
4. You'll see:
   - Navigation bar with "Students", "Results", "Statistics", "My Details" (admin)
   - Access to all features
   - Can view all students and results

#### Student Login:
1. Click "Login" button
2. Select "Student" role  
3. Enter: cse0001 / pass123
4. You'll see:
   - Navigation bar with "My Details" only
   - Can only view own profile and results
   - Cannot access other students' data

#### Public Access:
1. Don't login
2. Can view "Students" and "Statistics" pages
3. Cannot access "Results" or "Student Dashboard"
4. Navigation shows "Login" button

## Security Features

### Session Management
- **Secure Cookies**: Session IDs stored as HTTP-only cookies
- **Session Timeout**: 1 hour inactivity timeout
- **Session Cleanup**: Expired sessions are automatically removed

### Access Control
- **Role Verification**: Every request checks user role
- **Data Isolation**: Students can only see their own data
- **Protected Routes**: Admin-only and student-only endpoints
- **Logout**: Clears session immediately

### Database Integrity
- **Linked Accounts**: Student accounts linked to student roll numbers
- **Role Validation**: Prevents role mismatch exploitation
- **Foreign Keys**: Student accounts reference student records

## Implementation Details

### Session Storage
```python
SESSIONS = {
    'session_id': {
        'username': 'cse0001',
        'role': 'student',
        'student_roll_no': 'CSE0001',
        'timestamp': 1234567890
    }
}
```

### Session Functions
- `create_session()` - Create new session with user data
- `get_session()` - Retrieve session if valid and not expired
- `destroy_session()` - Remove session on logout

### Navigation Bar
- Dynamic based on login status
- Admin: Shows all menu options
- Student: Shows only "My Details"
- Public: Shows "Login" button

## Code Structure

### New Methods in StudentRequestHandler
- `do_POST()` - Handle login form submission
- `get_session_cookie()` - Extract session ID from cookies
- `set_session_cookie()` - Set session ID in response
- `send_response_html()` - Send HTML with optional session cookie
- `get_nav_html()` - Generate navigation based on session
- `handle_login_page()` - Display login form
- `handle_login_submit()` - Process login
- `handle_logout()` - Clear session
- `handle_student_dashboard()` - Student profile page
- `handle_statistics_complete()` - Statistics with auth

### Updated Methods
- `do_GET()` - Now extracts session from cookies
- `handle_home()` - Shows different content based on login
- `handle_students_list()` - Blocks student access
- `handle_student_results()` - Blocks student access
- `get_nav_html()` - Displays role-based navigation

## Example Flow

### Student Login Flow
1. User visits http://localhost:8000
2. Clicks "Login" button
3. Selects "Student" role
4. Enters cse0001 / pass123
5. Server creates session and sets cookie
6. Redirects to home page
7. Navigation bar shows "My Details" and "Logout"
8. Clicking "My Details" shows only their profile
9. Cannot access /students or /student-results routes

### Admin Features
1. Admin logs in with admin / admin123
2. Can access all routes
3. Can view all students
4. Can see statistics
5. Can view any student's results by roll number
