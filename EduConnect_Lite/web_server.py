"""
WEB_SERVER.PY - Simple HTTP Web Server
=======================================
UNIT 4: Simple web programming using Python http.server

This file contains:
1. HTTP Server for displaying student data and results
2. Simple HTML pages
3. GET request handlers
"""

# Import required modules
import http.server              # UNIT 4: HTTP server module
import socketserver             # For server socket handling
import urllib.parse             # For parsing URL parameters
from database import db         # Import database module
import threading                # UNIT 3: Threading for running server
from http.cookies import SimpleCookie  # For session management
import hashlib                  # For session hashing
import time                     # For session expiry


# Session storage (in-memory for this simple implementation)
SESSIONS = {}  # Format: {session_id: {user_data, timestamp}}
SESSION_TIMEOUT = 3600  # 1 hour in seconds


def create_session(username, role, student_roll_no=None):
    """
    Create a new session for a user
    
    Parameters:
        username (str): Username
        role (str): User role (admin or student)
        student_roll_no (str): Student roll number if applicable
        
    Returns:
        str: Session ID
    """
    session_id = hashlib.md5(f"{username}{time.time()}".encode()).hexdigest()
    SESSIONS[session_id] = {
        'username': username,
        'role': role,
        'student_roll_no': student_roll_no,
        'timestamp': time.time()
    }
    return session_id


def get_session(session_id):
    """
    Get session data if valid
    
    Parameters:
        session_id (str): Session ID
        
    Returns:
        dict: Session data or None if expired/invalid
    """
    if session_id in SESSIONS:
        session = SESSIONS[session_id]
        # Check if session has expired
        if time.time() - session['timestamp'] < SESSION_TIMEOUT:
            return session
        else:
            # Remove expired session
            del SESSIONS[session_id]
    return None


def destroy_session(session_id):
    """Remove a session"""
    if session_id in SESSIONS:
        del SESSIONS[session_id]


# ============================================================================
# UNIT 4: HTTP REQUEST HANDLER CLASS
# ============================================================================

class StudentRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    UNIT 4: Custom HTTP request handler with authentication
    Handles GET and POST requests with session management
    """
    
    def do_GET(self):
        """
        UNIT 4: Handle GET requests
        This method is called when a client sends a GET request to the server
        """
        
        # Parse the URL to extract path and query parameters
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query_params = urllib.parse.parse_qs(parsed_url.query)
        
        # Get session from cookies
        session_id = self.get_session_cookie()
        session = get_session(session_id) if session_id else None
        
        # Route the request to appropriate handler
        if path == '/':
            self.handle_home(session)
        elif path == '/login':
            self.handle_login_page()
        elif path == '/logout':
            self.handle_logout(session_id)
        elif path == '/students':
            self.handle_students_list(session)
        elif path == '/student-results':
            self.handle_student_results(query_params, session)
        elif path == '/student-dashboard':
            self.handle_student_dashboard(session)
        elif path == '/statistics':
            self.handle_statistics_complete(session)
        else:
            self.handle_404()
    
    def do_POST(self):
        """
        UNIT 4: Handle POST requests for login
        """
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        
        if path == '/login':
            # Read POST data
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = urllib.parse.parse_qs(post_data)
            
            username = params.get('username', [''])[0]
            password = params.get('password', [''])[0]
            
            self.handle_login_submit(username, password)
        else:
            self.handle_404()
    
    def get_session_cookie(self):
        """Extract session ID from cookies"""
        cookies = SimpleCookie()
        if 'Cookie' in self.headers:
            cookies.load(self.headers['Cookie'])
            if 'session_id' in cookies:
                return cookies['session_id'].value
        return None
    
    def set_session_cookie(self, session_id):
        """Set session cookie in response"""
        cookie = SimpleCookie()
        cookie['session_id'] = session_id
        cookie['session_id']['path'] = '/'
        cookie['session_id']['max-age'] = SESSION_TIMEOUT
        return cookie.output(header='')
    
    # ====================================================================
    # UNIT 4: HTML Response Methods
    # ====================================================================
    
    def send_response_html(self, content, session_id=None, status_code=200):
        """
        Send HTML response to client
        
        Parameters:
            content (str): HTML content to send
            session_id (str): Session ID to set as cookie
            status_code (int): HTTP status code
        """
        # Send HTTP response code
        self.send_response(status_code)
        
        # Set content type to HTML
        self.send_header('Content-type', 'text/html; charset=utf-8')
        
        # Set session cookie if provided
        if session_id:
            self.send_header('Set-Cookie', f'session_id={session_id}; Path=/; Max-Age={SESSION_TIMEOUT}')
        
        # End of headers
        self.end_headers()
        
        # Send the content as response body
        self.wfile.write(content.encode('utf-8'))
    
    def get_nav_html(self, session):
        """Generate navigation HTML based on session"""
        if not session:
            return """
            <div class="navbar">
                <a href="/">Home</a>
                <a href="/login" style="float: right; background-color: #28a745;">Login</a>
            </div>
            """
        elif session['role'] == 'admin':
            return f"""
            <div class="navbar">
                <a href="/">Home</a>
                <a href="/students">Students</a>
                <a href="/statistics">Statistics</a>
                <a href="/student-results">Results</a>
                <span style="float: right;">Admin: {session['username']}</span>
                <a href="/logout" style="float: right; background-color: #dc3545; margin-right: 10px;">Logout</a>
            </div>
            """
        else:  # student
            return f"""
            <div class="navbar">
                <a href="/">Home</a>
                <a href="/student-dashboard">My Details</a>
                <span style="float: right;">Student: {session['username']}</span>
                <a href="/logout" style="float: right; background-color: #dc3545; margin-right: 10px;">Logout</a>
            </div>
            """
    
    # ====================================================================
    # Route Handlers
    # ====================================================================
    
    def handle_home(self, session):
        """
        UNIT 4: Handle home page request
        Shows different content for logged in vs non-logged in users
        """
        nav_html = self.get_nav_html(session)
        
        if not session:
            content = f"""
            <h2>📋 Available Pages:</h2>
            <ul class="menu">
                <li><a href="/students">View All Students (Public)</a></li>
                <li><a href="/statistics">View Statistics (Public)</a></li>
                <li><a href="/login">Login as Admin or Student</a></li>
            </ul>
            """
        elif session['role'] == 'admin':
            content = f"""
            <h2>👨‍💼 Admin Dashboard</h2>
            <ul class="menu">
                <li><a href="/students">View All Students</a></li>
                <li><a href="/statistics">View Statistics</a></li>
                <li><a href="/student-results">View Student Results</a></li>
            </ul>
            """
        else:  # student
            content = f"""
            <h2>🎓 Student Portal</h2>
            <p>Welcome, <strong>{session['username']}</strong>!</p>
            <ul class="menu">
                <li><a href="/student-dashboard">View My Details & Results</a></li>
            </ul>
            """
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>EduConnect Lite - Student Management</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; }}
                .navbar {{ 
                    background-color: #007bff; 
                    padding: 15px 20px;
                    color: white;
                    overflow: hidden;
                    border-bottom: 3px solid #0056b3;
                }}
                .navbar a {{ 
                    color: white; 
                    text-decoration: none; 
                    padding: 10px 15px;
                    display: inline-block;
                    border-radius: 3px;
                    margin-right: 5px;
                }}
                .navbar a:hover {{ background-color: #0056b3; }}
                .navbar span {{ margin-right: 10px; }}
                .container {{ max-width: 800px; margin: 20px auto; background-color: white; padding: 20px; border-radius: 5px; }}
                h1 {{ color: #333; margin-bottom: 10px; }}
                h2 {{ color: #007bff; margin-top: 20px; margin-bottom: 10px; }}
                .menu {{ list-style: none; padding: 0; }}
                .menu li {{ margin: 10px 0; }}
                .menu a {{ 
                    display: block; 
                    padding: 10px; 
                    background-color: #007bff; 
                    color: white; 
                    text-decoration: none;
                    border-radius: 3px;
                }}
                .menu a:hover {{ background-color: #0056b3; }}
                p {{ color: #666; margin: 10px 0; }}
            </style>
        </head>
        <body>
            {nav_html}
            <div class="container">
                <h1>🎓 EduConnect Lite - Student Management System</h1>
                <p>Simple Student Management Web Portal</p>
                {content}
                <hr style="margin-top: 30px; color: #ddd;">
                <p><small>Powered by Python HTTP Server</small></p>
            </div>
        </body>
        </html>
        """
        self.send_response_html(html)
    
    def handle_students_list(self, session):
        """
        UNIT 4: Handle request to view all students
        Only accessible to admin or public view
        """
        # Check if student is trying to access (not allowed)
        if session and session['role'] == 'student':
            return self.send_response_html("""
            <!DOCTYPE html>
            <html>
            <head><title>Access Denied</title></head>
            <body>
                <h1>❌ Access Denied</h1>
                <p>Students cannot view all students. Please use <a href="/student-dashboard">My Details</a> instead.</p>
                <a href="/">← Back to Home</a>
            </body>
            </html>
            """)
        
        nav_html = self.get_nav_html(session)
        
        # Get all students from database
        students = db.get_all_students()
        
        # UNIT 1: List comprehension to build table rows
        # This creates HTML row elements for each student
        rows = ''.join([
            f"""
            <tr>
                <td>{student['roll_no']}</td>
                <td>{student['name']}</td>
                <td>{student['email']}</td>
                <td>{student['phone']}</td>
                <td>{student['department']}</td>
                <td>{student['cgpa']}</td>
            </tr>
            """
            for student in students
        ])
        
        # Create HTML table
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>All Students - EduConnect Lite</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; }}
                .navbar {{ 
                    background-color: #007bff; 
                    padding: 15px 20px;
                    color: white;
                    overflow: hidden;
                    border-bottom: 3px solid #0056b3;
                }}
                .navbar a {{ 
                    color: white; 
                    text-decoration: none; 
                    padding: 10px 15px;
                    display: inline-block;
                    border-radius: 3px;
                    margin-right: 5px;
                }}
                .navbar a:hover {{ background-color: #0056b3; }}
                .navbar span {{ margin-right: 10px; }}
                .container {{ max-width: 1000px; margin: 20px auto; background-color: white; padding: 20px; border-radius: 5px; }}
                h1 {{ color: #333; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th {{ background-color: #007bff; color: white; padding: 10px; text-align: left; }}
                td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
                tr:hover {{ background-color: #f5f5f5; }}
                .back-link {{ margin-top: 20px; }}
                .back-link a {{ color: #007bff; text-decoration: none; margin-right: 15px; }}
                .back-link a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            {nav_html}
            <div class="container">
                <h1>👥 All Students ({len(students)})</h1>
                
                <table>
                    <tr>
                        <th>Roll Number</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Phone</th>
                        <th>Department</th>
                        <th>CGPA</th>
                    </tr>
                    {rows}
                </table>
                
                <div class="back-link">
                    <a href="/">← Back to Home</a>
                </div>
            </div>
        </body>
        </html>
        """
        self.send_response_html(html)
    
    def handle_student_results(self, query_params, session):
        """
        UNIT 4: Handle request to view student results
        
        Parameters:
            query_params (dict): URL query parameters
            session (dict): Current session
        """
        # Check if student is trying to access (not allowed)
        if session and session['role'] == 'student':
            return self.send_response_html("""
            <!DOCTYPE html>
            <html>
            <head><title>Access Denied</title></head>
            <body>
                <h1>❌ Access Denied</h1>
                <p>Students cannot view other students' results. Please use <a href="/student-dashboard">My Details</a> instead.</p>
                <a href="/">← Back to Home</a>
            </body>
            </html>
            """)
        
        nav_html = self.get_nav_html(session)
        
        # Extract roll number from query parameters
        roll_no = query_params.get('roll_no', [None])[0]
        
        if not roll_no:
            # If no roll number provided, show form
            students = db.get_all_students()
            options = ''.join([
                f"<option value=\"{s['roll_no']}\">{s['roll_no']} - {s['name']}</option>"
                for s in students
            ])
            
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Student Results - EduConnect Lite</title>
                <style>
                    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                    body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; }}
                    .navbar {{ 
                        background-color: #007bff; 
                        padding: 15px 20px;
                        color: white;
                        overflow: hidden;
                        border-bottom: 3px solid #0056b3;
                    }}
                    .navbar a {{ 
                        color: white; 
                        text-decoration: none; 
                        padding: 10px 15px;
                        display: inline-block;
                        border-radius: 3px;
                        margin-right: 5px;
                    }}
                    .navbar a:hover {{ background-color: #0056b3; }}
                    .navbar span {{ margin-right: 10px; }}
                    .container {{ max-width: 600px; margin: 20px auto; background-color: white; padding: 20px; border-radius: 5px; }}
                    h1 {{ color: #333; }}
                    form {{ margin-top: 20px; }}
                    label {{ display: block; margin: 10px 0 5px; }}
                    select, button {{ width: 100%; padding: 10px; margin-bottom: 10px; font-size: 14px; }}
                    button {{ background-color: #007bff; color: white; border: none; border-radius: 3px; cursor: pointer; }}
                    button:hover {{ background-color: #0056b3; }}
                    .back-link {{ margin-top: 20px; }}
                    .back-link a {{ color: #007bff; text-decoration: none; }}
                </style>
            </head>
            <body>
                {nav_html}
                <div class="container">
                    <h1>📊 View Student Results</h1>
                    
                    <form method="GET" action="/student-results">
                        <label for="roll_no">Select Student:</label>
                        <select name="roll_no" id="roll_no">
                            <option value="">-- Choose a Student --</option>
                            {options}
                        </select>
                        <button type="submit">View Results</button>
                    </form>
                    
                    <div class="back-link">
                        <a href="/">← Back to Home</a>
                    </div>
                </div>
            </body>
            </html>
            """
        else:
            # Show results for selected student
            student = db.get_student_by_roll_no(roll_no)
            
            if not student:
                html = f"""
                <!DOCTYPE html>
                <html>
                <head><title>Student Results - EduConnect Lite</title></head>
                <body>
                    {nav_html}
                    <div style="max-width: 800px; margin: 20px auto;">
                        <h1>❌ Student Not Found</h1>
                        <p>The student with roll number {roll_no} was not found.</p>
                        <a href="/student-results">← Try Again</a>
                    </div>
                </body>
                </html>
                """
            else:
                # Get student results from database
                results = db.get_student_results(roll_no)
                
                # UNIT 1: List comprehension to create result rows
                result_rows = ''.join([
                    f"""
                    <tr>
                        <td>{result['subject']}</td>
                        <td>{result['marks']}</td>
                    </tr>
                    """
                    for result in results
                ])
                
                if not results:
                    result_rows = '<tr><td colspan="2">No results available</td></tr>'
                
                html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Student Results - EduConnect Lite</title>
                    <style>
                        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                        body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; }}
                        .navbar {{ 
                            background-color: #007bff; 
                            padding: 15px 20px;
                            color: white;
                            overflow: hidden;
                            border-bottom: 3px solid #0056b3;
                        }}
                        .navbar a {{ 
                            color: white; 
                            text-decoration: none; 
                            padding: 10px 15px;
                            display: inline-block;
                            border-radius: 3px;
                            margin-right: 5px;
                        }}
                        .navbar a:hover {{ background-color: #0056b3; }}
                        .navbar span {{ margin-right: 10px; }}
                        .container {{ max-width: 800px; margin: 20px auto; background-color: white; padding: 20px; border-radius: 5px; }}
                        h1 {{ color: #333; }}
                        .student-info {{ background-color: #e9ecef; padding: 10px; border-radius: 3px; margin: 10px 0; }}
                        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                        th {{ background-color: #007bff; color: white; padding: 10px; }}
                        td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
                        .back-link {{ margin-top: 20px; }}
                        .back-link a {{ color: #007bff; text-decoration: none; margin-right: 15px; }}
                    </style>
                </head>
                <body>
                    {nav_html}
                    <div class="container">
                        <h1>📊 Results for {student['name']}</h1>
                        
                        <div class="student-info">
                            <p><strong>Roll Number:</strong> {student['roll_no']}</p>
                            <p><strong>Department:</strong> {student['department']}</p>
                            <p><strong>CGPA:</strong> {student['cgpa']}</p>
                        </div>
                        
                        <h2>Semester Results:</h2>
                        <table>
                            <tr>
                                <th>Subject</th>
                                <th>Marks</th>
                            </tr>
                            {result_rows}
                        </table>
                        
                        <div class="back-link">
                            <a href="/student-results">← View Another Student</a>
                            <a href="/">← Back to Home</a>
                        </div>
                    </div>
                </body>
                </html>
                """
        
        self.send_response_html(html)
    
    def handle_student_dashboard(self, session):
        """
        UNIT 4: Handle student dashboard - shows only student's own details
        Only accessible to authenticated students
        """
        if not session:
            return self.send_response_html("""
            <!DOCTYPE html>
            <html>
            <head><title>Login Required</title></head>
            <body>
                <h1>❌ Login Required</h1>
                <p>Please <a href="/login">login</a> to view your details.</p>
            </body>
            </html>
            """)
        
        if session['role'] != 'student':
            return self.send_response_html("""
            <!DOCTYPE html>
            <html>
            <head><title>Access Denied</title></head>
            <body>
                <h1>❌ Access Denied</h1>
                <p>Only students can access this page.</p>
                <a href="/">← Back to Home</a>
            </body>
            </html>
            """)
        
        nav_html = self.get_nav_html(session)
        
        # Get student data
        roll_no = session.get('student_roll_no')
        student = db.get_student_by_roll_no(roll_no)
        
        if not student:
            return self.send_response_html(f"""
            <!DOCTYPE html>
            <html>
            <head><title>Student Not Found</title></head>
            <body>
                {nav_html}
                <div style="max-width: 800px; margin: 20px auto;">
                    <h1>❌ Student Record Not Found</h1>
                    <a href="/">← Back to Home</a>
                </div>
            </body>
            </html>
            """)
        
        # Get results
        results = db.get_student_results(roll_no)
        result_rows = ''.join([
            f"<tr><td>{r['subject']}</td><td>{r['marks']}/100</td></tr>"
            for r in results
        ])
        
        if not results:
            result_rows = '<tr><td colspan="2" style="text-align: center;">No results available</td></tr>'
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>My Details - EduConnect Lite</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; }}
                .navbar {{ 
                    background-color: #007bff; 
                    padding: 15px 20px;
                    color: white;
                    overflow: hidden;
                    border-bottom: 3px solid #0056b3;
                }}
                .navbar a {{ 
                    color: white; 
                    text-decoration: none; 
                    padding: 10px 15px;
                    display: inline-block;
                    border-radius: 3px;
                    margin-right: 5px;
                }}
                .navbar a:hover {{ background-color: #0056b3; }}
                .navbar span {{ margin-right: 10px; }}
                .container {{ max-width: 800px; margin: 20px auto; background-color: white; padding: 20px; border-radius: 5px; }}
                h1 {{ color: #333; margin-bottom: 20px; }}
                h2 {{ color: #007bff; margin-top: 30px; margin-bottom: 15px; }}
                .details-box {{ background-color: #e9ecef; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
                .details-box p {{ margin: 8px 0; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
                th {{ background-color: #007bff; color: white; padding: 10px; text-align: left; }}
                td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
                tr:hover {{ background-color: #f5f5f5; }}
                .back-link {{ margin-top: 30px; }}
                .back-link a {{ color: #007bff; text-decoration: none; margin-right: 15px; }}
            </style>
        </head>
        <body>
            {nav_html}
            <div class="container">
                <h1>🎓 My Student Profile</h1>
                
                <h2>📋 Personal Details</h2>
                <div class="details-box">
                    <p><strong>Roll Number:</strong> {student['roll_no']}</p>
                    <p><strong>Name:</strong> {student['name']}</p>
                    <p><strong>Email:</strong> {student['email']}</p>
                    <p><strong>Phone:</strong> {student['phone']}</p>
                    <p><strong>Department:</strong> {student['department']}</p>
                    <p><strong>CGPA:</strong> {student['cgpa']}</p>
                </div>
                
                <h2>📊 My Results</h2>
                <table>
                    <tr>
                        <th>Subject</th>
                        <th>Marks</th>
                    </tr>
                    {result_rows}
                </table>
                
                <div class="back-link">
                    <a href="/">← Back to Home</a>
                </div>
            </div>
        </body>
        </html>
        """
        self.send_response_html(html)
    
    def handle_login_page(self):
        """
        UNIT 4: Display login page
        """
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Login - EduConnect Lite</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; justify-content: center; align-items: center; }
                .login-container { background-color: white; padding: 40px; border-radius: 10px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); width: 100%; max-width: 400px; }
                h1 { color: #333; margin-bottom: 10px; text-align: center; }
                .subtitle { color: #666; text-align: center; margin-bottom: 30px; font-size: 14px; }
                .form-group { margin-bottom: 15px; }
                label { display: block; margin-bottom: 5px; color: #333; font-weight: bold; }
                input[type="text"], input[type="password"] { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 14px; }
                input[type="text"]:focus, input[type="password"]:focus { outline: none; border-color: #667eea; box-shadow: 0 0 5px rgba(102, 126, 234, 0.3); }
                .role-group { margin-bottom: 20px; }
                .role-option { margin: 10px 0; }
                .role-option input[type="radio"] { margin-right: 8px; }
                .role-option label { display: inline; margin: 0; }
                button { width: 100%; padding: 12px; background-color: #667eea; color: white; border: none; border-radius: 5px; font-size: 16px; font-weight: bold; cursor: pointer; }
                button:hover { background-color: #764ba2; }
                .back-link { text-align: center; margin-top: 20px; }
                .back-link a { color: #667eea; text-decoration: none; }
                .back-link a:hover { text-decoration: underline; }
                .credentials { background-color: #e9ecef; padding: 15px; border-radius: 5px; margin-top: 20px; font-size: 12px; }
                .credentials h3 { color: #333; margin-bottom: 10px; }
                .credentials p { margin: 5px 0; }
            </style>
        </head>
        <body>
            <div class="login-container">
                <h1>🎓 EduConnect Lite</h1>
                <div class="subtitle">Student Management System</div>
                
                <form method="POST" action="/login">
                    <div class="role-group">
                        <label>Login as:</label>
                        <div class="role-option">
                            <input type="radio" id="admin" name="role" value="admin" checked>
                            <label for="admin">Admin</label>
                        </div>
                        <div class="role-option">
                            <input type="radio" id="student" name="role" value="student">
                            <label for="student">Student</label>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label for="username">Username:</label>
                        <input type="text" id="username" name="username" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="password">Password:</label>
                        <input type="password" id="password" name="password" required>
                    </div>
                    
                    <button type="submit">Login</button>
                </form>
                
                <div class="credentials">
                    <h3>Demo Credentials:</h3>
                    <p><strong>Admin:</strong> admin / admin123</p>
                    <p><strong>Student 1:</strong> cse0001 / pass123</p>
                    <p><strong>Student 2:</strong> cse0002 / pass123</p>
                    <p><strong>Student 3:</strong> ece0001 / pass123</p>
                </div>
                
                <div class="back-link">
                    <a href="/">← Back to Home</a>
                </div>
            </div>
        </body>
        </html>
        """
        self.send_response_html(html)
    
    def handle_login_submit(self, username, password):
        """
        UNIT 4: Handle login form submission
        """
        # Verify credentials
        user = db.verify_login(username, password)
        
        if user:
            # Create session
            session_id = create_session(
                username,
                user['role'],
                user.get('student_roll_no')
            )
            
            # Redirect to home with session cookie
            self.send_response(302)
            self.send_header('Location', '/')
            self.send_header('Set-Cookie', f'session_id={session_id}; Path=/; Max-Age={SESSION_TIMEOUT}')
            self.end_headers()
        else:
            # Show login page with error
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Login Failed - EduConnect Lite</title>
                <style>
                    body {{ font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; justify-content: center; align-items: center; }}
                    .login-container {{ background-color: white; padding: 40px; border-radius: 10px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); width: 100%; max-width: 400px; }}
                    .error {{ background-color: #f8d7da; color: #721c24; padding: 12px; border-radius: 5px; margin-bottom: 20px; }}
                    .back-link {{ text-align: center; margin-top: 20px; }}
                    .back-link a {{ color: #667eea; text-decoration: none; }}
                </style>
            </head>
            <body>
                <div class="login-container">
                    <h1>❌ Login Failed</h1>
                    <div class="error">
                        <strong>Invalid Credentials!</strong><br>
                        Username or password is incorrect.
                    </div>
                    <div class="back-link">
                        <a href="/login">← Try Again</a><br>
                        <a href="/">← Back to Home</a>
                    </div>
                </div>
            </body>
            </html>
            """
            self.send_response_html(html, status_code=401)
    
    def handle_logout(self, session_id):
        """
        UNIT 4: Handle logout
        """
        if session_id:
            destroy_session(session_id)
        
        # Redirect to home
        self.send_response(302)
        self.send_header('Location', '/')
        self.send_header('Set-Cookie', 'session_id=; Path=/; Max-Age=0')
        self.end_headers()
    
    def handle_statistics_complete(self, session):
        """
        UNIT 4: Handle request to view statistics
        Complete version with authentication
        """
        if session and session['role'] == 'student':
            return self.send_response_html("""
            <!DOCTYPE html>
            <html>
            <head><title>Access Denied</title></head>
            <body>
                <h1>❌ Access Denied</h1>
                <p>Students cannot view statistics.</p>
                <a href="/">← Back to Home</a>
            </body>
            </html>
            """)
        
        nav_html = self.get_nav_html(session)
        
        stats = db.get_statistics()
        
        # Get students by department using list comprehension
        all_students = db.get_all_students()
        departments = {}
        
        # UNIT 1: Dictionary comprehension to group by department
        for student in all_students:
            dept = student['department']
            if dept not in departments:
                departments[dept] = 0
            departments[dept] += 1
        
        # Create department rows
        dept_rows = ''.join([
            f"<tr><td>{dept}</td><td>{count}</td></tr>"
            for dept, count in departments.items()
        ])
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Statistics - EduConnect Lite</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; }}
                .navbar {{ 
                    background-color: #007bff; 
                    padding: 15px 20px;
                    color: white;
                    overflow: hidden;
                    border-bottom: 3px solid #0056b3;
                }}
                .navbar a {{ 
                    color: white; 
                    text-decoration: none; 
                    padding: 10px 15px;
                    display: inline-block;
                    border-radius: 3px;
                    margin-right: 5px;
                }}
                .navbar a:hover {{ background-color: #0056b3; }}
                .navbar span {{ margin-right: 10px; }}
                .container {{ max-width: 800px; margin: 20px auto; background-color: white; padding: 20px; border-radius: 5px; }}
                h1 {{ color: #333; }}
                .stats-box {{ 
                    display: inline-block; 
                    background-color: #e9ecef; 
                    padding: 20px; 
                    margin: 10px;
                    border-radius: 5px;
                    min-width: 200px;
                    text-align: center;
                }}
                .stats-box h3 {{ color: #007bff; margin: 0; }}
                .stats-box .value {{ font-size: 28px; font-weight: bold; color: #333; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th {{ background-color: #007bff; color: white; padding: 10px; }}
                td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
                .back-link {{ margin-top: 20px; }}
                .back-link a {{ color: #007bff; text-decoration: none; margin-right: 15px; }}
            </style>
        </head>
        <body>
            {nav_html}
            <div class="container">
                <h1>📊 Database Statistics</h1>
                
                <div style="text-align: center;">
                    <div class="stats-box">
                        <h3>Total Students</h3>
                        <div class="value">{stats.get('total_students', 0)}</div>
                    </div>
                    <div class="stats-box">
                        <h3>Average CGPA</h3>
                        <div class="value">{stats.get('average_cgpa', 0)}</div>
                    </div>
                    <div class="stats-box">
                        <h3>Departments</h3>
                        <div class="value">{stats.get('departments', 0)}</div>
                    </div>
                </div>
                
                <h2>Students by Department:</h2>
                <table>
                    <tr>
                        <th>Department</th>
                        <th>Count</th>
                    </tr>
                    {dept_rows}
                </table>
                
                <div class="back-link">
                    <a href="/">← Back to Home</a>
                </div>
            </div>
        </body>
        </html>
        """
        self.send_response_html(html)
    
    def handle_statistics(self):
        """
        UNIT 4: Handle request to view statistics
        """
        stats = db.get_statistics()
        
        # Get students by department using list comprehension
        all_students = db.get_all_students()
        departments = {}
        
        # UNIT 1: Dictionary comprehension to group by department
        for student in all_students:
            dept = student['department']
            if dept not in departments:
                departments[dept] = 0
            departments[dept] += 1
        
        # Create department rows
        dept_rows = ''.join([
            f"<tr><td>{dept}</td><td>{count}</td></tr>"
            for dept, count in departments.items()
        ])
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Statistics - EduConnect Lite</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f4; }}
                .container {{ max-width: 800px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 5px; }}
                h1 {{ color: #333; }}
                .stats-box {{ 
                    display: inline-block; 
                    background-color: #e9ecef; 
                    padding: 20px; 
                    margin: 10px;
                    border-radius: 5px;
                    min-width: 200px;
                    text-align: center;
                }}
                .stats-box h3 {{ color: #007bff; margin: 0; }}
                .stats-box .value {{ font-size: 28px; font-weight: bold; color: #333; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th {{ background-color: #007bff; color: white; padding: 10px; }}
                td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
                .back-link {{ margin-top: 20px; }}
                .back-link a {{ color: #007bff; text-decoration: none; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Database Statistics</h1>
                
                <div style="text-align: center;">
                    <div class="stats-box">
                        <h3>Total Students</h3>
                        <div class="value">{stats.get('total_students', 0)}</div>
                    </div>
                    <div class="stats-box">
                        <h3>Average CGPA</h3>
                        <div class="value">{stats.get('average_cgpa', 0)}</div>
                    </div>
                    <div class="stats-box">
                        <h3>Departments</h3>
                        <div class="value">{stats.get('departments', 0)}</div>
                    </div>
                </div>
                
                <h2>Students by Department:</h2>
                <table>
                    <tr>
                        <th>Department</th>
                        <th>Count</th>
                    </tr>
                    {dept_rows}
                </table>
                
                <div class="back-link">
                    <a href="/">← Back to Home</a>
                </div>
            </div>
        </body>
        </html>
        """
        self.send_response_html(html)
    
    def handle_404(self):
        """
        Handle 404 - Page Not Found
        """
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>404 - Not Found</title>
            <style>
                body { font-family: Arial, sans-serif; background-color: #f4f4f4; }
                .container { max-width: 600px; margin: 50px auto; background-color: white; padding: 40px; border-radius: 5px; text-align: center; }
                h1 { color: #dc3545; }
                a { color: #007bff; text-decoration: none; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>❌ 404 - Page Not Found</h1>
                <p>The page you requested does not exist.</p>
                <a href="/">← Go to Home</a>
            </div>
        </body>
        </html>
        """
        
        self.wfile.write(html.encode('utf-8'))
    
    # Override logging to reduce console output
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass


# ============================================================================
# UNIT 3: WEB SERVER STARTUP - Using Threading
# ============================================================================

def start_web_server(host='localhost', port=8000):
    """
    UNIT 3: Start web server in a separate thread
    Uses threading to run server without blocking main program
    
    Parameters:
        host (str): Server host address
        port (int): Server port number
    """
    try:
        # UNIT 4: Create HTTP server with custom request handler
        handler = StudentRequestHandler
        httpd = socketserver.TCPServer((host, port), handler)
        
        server_address = f"http://{host}:{port}"
        print(f"✓ Web server started: {server_address}")
        print(f"  Open your browser and navigate to {server_address}")
        
        # UNIT 3: Start server in a separate thread (daemon thread)
        # This allows the GUI to continue running
        server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        server_thread.start()
        
        return httpd
        
    except Exception as e:
        print(f"✗ Error starting web server: {str(e)}")
        return None


def start_web_server_blocking(host='localhost', port=8000):
    """
    Start web server in blocking mode (for command-line use)
    
    Parameters:
        host (str): Server host address
        port (int): Server port number
    """
    try:
        handler = StudentRequestHandler
        httpd = socketserver.TCPServer((host, port), handler)
        
        print(f"\n✓ Web server running at: http://{host}:{port}")
        print(f"  Press CTRL+C to stop the server\n")
        
        # This blocks - server runs until interrupted
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        print("\n✓ Web server stopped")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
