# Student Management System

A comprehensive web-based student management system built with Python Flask and MySQL.

## Features

### Admin Portal
- Manage students, faculty, and courses
- View system statistics
- Fee management
- Generate reports

### Student Portal
- View enrolled courses
- Check attendance records
- View grades and GPA
- Fee status

### Faculty Portal
- View assigned courses
- Mark attendance
- Add and manage grades
- Student reports

## Database Schema

### Tables
1. **Users** - User authentication (admin, student, faculty)
2. **Students** - Student personal information
3. **Faculty** - Faculty details
4. **Courses** - Course catalog
5. **Enrollment** - Student course enrollment
6. **Attendance** - Attendance records
7. **Grades** - Student grades and assessments
8. **Fees** - Fee management
9. **Announcements** - System announcements
10. **Timetable** - Class schedule

## Technology Stack

- **Backend**: Python 3.x, Flask Framework
- **Database**: MySQL 8.0
- **Frontend**: HTML5, CSS3, Jinja2 Templates
- **Database Connector**: mysql-connector-python

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- MySQL 8.0 or higher
- pip (Python package manager)

### Step 1: Database Setup

1. Open MySQL Command Line Client or MySQL Workbench
2. Execute the SQL files in order:

```sql
source C:/Coding/Student_Management_System/database/01_schema.sql
source C:/Coding/Student_Management_System/database/02_sample_data.sql
source C:/Coding/Student_Management_System/database/03_procedures_functions.sql
```

Or manually:
- Run `01_schema.sql` to create database and tables
- Run `02_sample_data.sql` to insert sample data
- Run `03_procedures_functions.sql` to create stored procedures

### Step 2: Python Environment Setup

1. Open PowerShell/Command Prompt
2. Navigate to project directory:
```powershell
cd C:\Coding\Student_Management_System
```

3. Install required packages:
```powershell
pip install -r requirements.txt
```

### Step 3: Configure Database Connection

Edit `backend/database.py` and update MySQL credentials:

```python
self.host = 'localhost'
self.database = 'student_management_system'
self.user = 'root'
self.password = 'YOUR_MYSQL_PASSWORD'  # Change this!
```

### Step 4: Run the Application

```powershell
cd backend
python app.py
```

The application will start at: `http://localhost:5000`

## Default Login Credentials

### Admin Access
- **Username**: admin
- **Password**: admin123

### Student Access
- **Username**: john.student
- **Password**: pass123

### Faculty Access
- **Username**: dr.smith
- **Password**: faculty123

## Project Structure

```
Student_Management_System/
│
├── database/
│   ├── 01_schema.sql              # Database schema
│   ├── 02_sample_data.sql         # Sample data
│   └── 03_procedures_functions.sql # Stored procedures
│
├── backend/
│   ├── app.py                     # Flask application
│   └── database.py                # Database connection
│
├── templates/
│   ├── base.html                  # Base template
│   ├── index.html                 # Home page
│   ├── login.html                 # Login page
│   ├── admin/                     # Admin templates
│   ├── student/                   # Student templates
│   └── faculty/                   # Faculty templates
│
├── static/
│   └── css/
│       └── style.css              # Stylesheet
│
└── requirements.txt               # Python dependencies
```

## Database ER Diagram (Text Representation)

```
Users (1) ──────(1) Students
Users (1) ──────(1) Faculty

Students (M) ──────(M) Courses [through Enrollment]
Students (1) ──────(M) Attendance
Students (1) ──────(M) Grades
Students (1) ──────(M) Fees

Faculty (1) ──────(M) Course_Assignment
Courses (1) ──────(M) Course_Assignment
Courses (1) ──────(M) Enrollment
Courses (1) ──────(M) Attendance
Courses (1) ──────(M) Grades
Courses (1) ──────(M) Timetable
```

## Key Features Implementation

### Stored Procedures
- `sp_AddStudent` - Add new student with user account
- `sp_EnrollStudent` - Enroll student in course
- `sp_MarkAttendance` - Mark student attendance
- `sp_AddGrade` - Add student grades
- `sp_GetStudentCourses` - Get enrolled courses
- `sp_GetAttendanceReport` - Attendance report

### Functions
- `fn_CalculateGPA` - Calculate student GPA

### Triggers
- `tr_UpdateFeeStatus` - Auto-update fee status

## Usage Guide

### For Admin
1. Login with admin credentials
2. Navigate to Manage Students/Faculty/Courses
3. Add new records using the "Add New" button
4. View and manage all system data

### For Students
1. Login with student credentials
2. View dashboard for personal info and courses
3. Check attendance and grades
4. View timetable and announcements

### For Faculty
1. Login with faculty credentials
2. View assigned courses
3. Mark attendance for classes
4. Add grades for assessments

## Screenshots

*Note: Take screenshots after running the application and navigating through different pages*

Required screenshots for project report:
1. Home page
2. Login page
3. Admin dashboard
4. Student list
5. Add student form
6. Course list
7. Add course form
8. Student dashboard
9. Student attendance view
10. Student grades view
11. Faculty dashboard
12. Mark attendance form
13. Add grades form

## Future Enhancements

- Email notifications
- PDF report generation
- Advanced analytics
- Online exam module
- Library management integration
- Parent portal

## Troubleshooting

### Database Connection Error
- Check MySQL is running
- Verify database credentials in `database.py`
- Ensure database exists: `student_management_system`

### Module Not Found Error
- Install requirements: `pip install -r requirements.txt`

### Port Already in Use
- Change port in `app.py`: `app.run(debug=True, port=5001)`

## Contributors

- Pranvkumar Kshirsagar
- SAP ID: 590011587

## License

This project is for educational purposes.

---

For any questions or issues, please contact: [Your Email]
