from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import DatabaseConnection
from datetime import datetime

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = 'your_secret_key_here_change_this'

db = DatabaseConnection()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        query = "SELECT * FROM Users WHERE username = %s AND password = %s"
        user = db.execute_query(query, (username, password))
        
        if user and len(user) > 0:
            session['user_id'] = user[0]['user_id']
            session['username'] = user[0]['username']
            session['role'] = user[0]['role']
            
            if user[0]['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user[0]['role'] == 'student':
                return redirect(url_for('student_dashboard'))
            elif user[0]['role'] == 'faculty':
                return redirect(url_for('faculty_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    stats = {}
    stats['total_students'] = db.execute_query("SELECT COUNT(*) as count FROM Students")[0]['count']
    stats['total_faculty'] = db.execute_query("SELECT COUNT(*) as count FROM Faculty")[0]['count']
    stats['total_courses'] = db.execute_query("SELECT COUNT(*) as count FROM Courses")[0]['count']
    
    return render_template('admin/dashboard.html', stats=stats)

@app.route('/admin/students')
def admin_students():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    students = db.execute_query("SELECT * FROM Students ORDER BY student_id DESC")
    return render_template('admin/students.html', students=students)

@app.route('/admin/students/add', methods=['GET', 'POST'])
def admin_add_student():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        gender = request.form['gender']
        phone = request.form['phone']
        address = request.form['address']
        program = request.form['program']
        semester = request.form['semester']
        
        result = db.call_procedure('sp_AddStudent', (username, password, email, first_name, last_name, dob, gender, phone, address, program, semester))
        
        if result:
            flash('Student added successfully!', 'success')
            return redirect(url_for('admin_students'))
        else:
            flash('Error adding student', 'error')
    
    return render_template('admin/add_student.html')

@app.route('/admin/faculty')
def admin_faculty():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    faculty = db.execute_query("SELECT * FROM Faculty ORDER BY faculty_id DESC")
    return render_template('admin/faculty.html', faculty=faculty)

@app.route('/admin/courses')
def admin_courses():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    courses = db.execute_query("SELECT * FROM Courses ORDER BY course_id DESC")
    return render_template('admin/courses.html', courses=courses)

@app.route('/admin/courses/add', methods=['GET', 'POST'])
def admin_add_course():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        course_code = request.form['course_code']
        course_name = request.form['course_name']
        credits = request.form['credits']
        department = request.form['department']
        semester = request.form['semester']
        description = request.form['description']
        
        query = """INSERT INTO Courses (course_code, course_name, credits, department, semester, description)
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        result = db.execute_query(query, (course_code, course_name, credits, department, semester, description))
        
        if result:
            flash('Course added successfully!', 'success')
            return redirect(url_for('admin_courses'))
        else:
            flash('Error adding course', 'error')
    
    return render_template('admin/add_course.html')

@app.route('/student/dashboard')
def student_dashboard():
    if 'role' not in session or session['role'] != 'student':
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    student = db.execute_query("SELECT * FROM Students WHERE user_id = %s", (user_id,))[0]
    student_id = student['student_id']
    
    courses = db.call_procedure('sp_GetStudentCourses', (student_id,))
    
    return render_template('student/dashboard.html', student=student, courses=courses)

@app.route('/student/attendance')
def student_attendance():
    if 'role' not in session or session['role'] != 'student':
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    student = db.execute_query("SELECT * FROM Students WHERE user_id = %s", (user_id,))[0]
    student_id = student['student_id']
    
    query = """SELECT c.course_name, c.course_code,
                      COUNT(*) AS total_classes,
                      SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) AS attended,
                      ROUND((SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS percentage
               FROM Attendance a
               JOIN Courses c ON a.course_id = c.course_id
               WHERE a.student_id = %s
               GROUP BY c.course_id"""
    
    attendance = db.execute_query(query, (student_id,))
    
    return render_template('student/attendance.html', attendance=attendance)

@app.route('/student/grades')
def student_grades():
    if 'role' not in session or session['role'] != 'student':
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    student = db.execute_query("SELECT * FROM Students WHERE user_id = %s", (user_id,))[0]
    student_id = student['student_id']
    
    query = """SELECT c.course_name, g.assessment_type, g.marks_obtained, g.max_marks, g.grade_letter
               FROM Grades g
               JOIN Courses c ON g.course_id = c.course_id
               WHERE g.student_id = %s
               ORDER BY g.grade_id DESC"""
    
    grades = db.execute_query(query, (student_id,))
    
    return render_template('student/grades.html', grades=grades)

@app.route('/faculty/dashboard')
def faculty_dashboard():
    if 'role' not in session or session['role'] != 'faculty':
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    faculty = db.execute_query("SELECT * FROM Faculty WHERE user_id = %s", (user_id,))[0]
    faculty_id = faculty['faculty_id']
    
    query = """SELECT c.* FROM Courses c
               JOIN Course_Assignment ca ON c.course_id = ca.course_id
               WHERE ca.faculty_id = %s"""
    
    courses = db.execute_query(query, (faculty_id,))
    
    return render_template('faculty/dashboard.html', faculty=faculty, courses=courses)

@app.route('/faculty/attendance/<int:course_id>', methods=['GET', 'POST'])
def faculty_mark_attendance(course_id):
    if 'role' not in session or session['role'] != 'faculty':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        date = request.form['date']
        attendance_data = request.form.to_dict()
        
        for key, value in attendance_data.items():
            if key.startswith('student_'):
                student_id = key.split('_')[1]
                result = db.call_procedure('sp_MarkAttendance', (student_id, course_id, date, value))
        
        flash('Attendance marked successfully!', 'success')
        return redirect(url_for('faculty_dashboard'))
    
    query = """SELECT s.* FROM Students s
               JOIN Enrollment e ON s.student_id = e.student_id
               WHERE e.course_id = %s AND e.status = 'Enrolled'"""
    
    students = db.execute_query(query, (course_id,))
    course = db.execute_query("SELECT * FROM Courses WHERE course_id = %s", (course_id,))[0]
    
    return render_template('faculty/mark_attendance.html', students=students, course=course)

@app.route('/faculty/grades/<int:course_id>', methods=['GET', 'POST'])
def faculty_add_grades(course_id):
    if 'role' not in session or session['role'] != 'faculty':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        student_id = request.form['student_id']
        assessment_type = request.form['assessment_type']
        marks_obtained = request.form['marks_obtained']
        max_marks = request.form['max_marks']
        academic_year = request.form['academic_year']
        
        result = db.call_procedure('sp_AddGrade', (student_id, course_id, assessment_type, marks_obtained, max_marks, academic_year))
        
        if result:
            flash('Grade added successfully!', 'success')
            return redirect(url_for('faculty_dashboard'))
        else:
            flash('Error adding grade', 'error')
    
    query = """SELECT s.* FROM Students s
               JOIN Enrollment e ON s.student_id = e.student_id
               WHERE e.course_id = %s AND e.status = 'Enrolled'"""
    
    students = db.execute_query(query, (course_id,))
    course = db.execute_query("SELECT * FROM Courses WHERE course_id = %s", (course_id,))[0]
    
    return render_template('faculty/add_grades.html', students=students, course=course)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
