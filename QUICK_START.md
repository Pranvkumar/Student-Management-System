# Quick Start Guide

## Step-by-Step Setup (5 Minutes)

### 1. Setup Database (2 minutes)

Open MySQL terminal and run:

```sql
source C:/Coding/Student_Management_System/database/01_schema.sql
source C:/Coding/Student_Management_System/database/02_sample_data.sql
source C:/Coding/Student_Management_System/database/03_procedures_functions.sql
```

### 2. Install Python Packages (1 minute)

```powershell
cd C:\Coding\Student_Management_System
pip install -r requirements.txt
```

### 3. Configure Database Password (30 seconds)

Edit `backend/database.py` line 9:
```python
self.password = 'YOUR_MYSQL_ROOT_PASSWORD'
```

### 4. Run Application (30 seconds)

```powershell
cd backend
python app.py
```

### 5. Open Browser

Navigate to: `http://localhost:5000`

Login with:
- Admin: `admin` / `admin123`
- Student: `john.student` / `pass123`
- Faculty: `dr.smith` / `faculty123`

## Taking Screenshots for Report

### Required Pages (13 screenshots minimum)

1. **Home Page** - `http://localhost:5000/`
2. **Login Page** - `http://localhost:5000/login`

#### Admin Portal (5 screenshots)
3. **Admin Dashboard** - Login as admin
4. **Students List** - Click "Manage Students"
5. **Add Student Form** - Click "Add New Student"
6. **Courses List** - Click "Manage Courses"
7. **Add Course Form** - Click "Add New Course"

#### Student Portal (3 screenshots)
8. **Student Dashboard** - Login as john.student
9. **Attendance View** - Click "My Attendance"
10. **Grades View** - Click "My Grades"

#### Faculty Portal (3 screenshots)
11. **Faculty Dashboard** - Login as dr.smith
12. **Mark Attendance** - Click "Mark Attendance" for any course
13. **Add Grades** - Click "Add Grades" for any course

## Screenshot Tips

- Use **Windows + Shift + S** to take clean screenshots
- Capture full browser window
- Show the URL bar
- Demonstrate different data in each view

## What's Working

✅ Complete database with 10 tables
✅ Sample data for testing
✅ User login (admin, student, faculty)
✅ Admin: Add students, courses, faculty
✅ Student: View courses, attendance, grades
✅ Faculty: Mark attendance, add grades
✅ Stored procedures for business logic
✅ Responsive design

## What You Need to Complete

The HTML templates are **static** (non-interactive). They show the structure and design.

### To Make Them Fully Functional:

1. **Connect Forms to Backend** - The forms are already connected via Flask routes in `app.py`
2. **Test All Features** - Run the app and test adding students, marking attendance, etc.
3. **Take Screenshots** - Screenshot every page after testing
4. **Customize Styling** - Edit `static/css/style.css` if needed

### Quick Testing Checklist

- [ ] Database created successfully
- [ ] Can login as admin
- [ ] Can view student list
- [ ] Can add new student
- [ ] Can login as student
- [ ] Can view attendance
- [ ] Can login as faculty
- [ ] Can mark attendance
- [ ] All 13 screenshots taken

## Common Issues

**Q: Database connection error?**
A: Check MySQL password in `backend/database.py`

**Q: Flask not found?**
A: Run `pip install -r requirements.txt`

**Q: Port 5000 busy?**
A: Change to 5001 in `app.py` last line

**Q: Data not showing?**
A: Check database has sample data: `SELECT COUNT(*) FROM Students;`

## Need Help?

Check `README.md` for detailed documentation!
