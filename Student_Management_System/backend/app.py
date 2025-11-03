from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import DatabaseConnection
from datetime import datetime
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = 'your_secret_key_here_change_this'

# Configure upload settings
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db = DatabaseConnection()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@app.route('/admin/students/upload', methods=['GET', 'POST'])
def admin_upload_students():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
            flash('No file uploaded', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        # Check if file type is allowed
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                # Read Excel file
                df = pd.read_excel(filepath)
                
                # Validate required columns
                required_columns = ['username', 'password', 'email', 'first_name', 'last_name', 
                                  'dob', 'gender', 'phone', 'address', 'program', 'semester']
                
                missing_columns = [col for col in required_columns if col not in df.columns]
                if missing_columns:
                    flash(f'Missing required columns: {", ".join(missing_columns)}', 'error')
                    os.remove(filepath)
                    return redirect(request.url)
                
                # Process each row
                success_count = 0
                error_count = 0
                errors = []
                
                for index, row in df.iterrows():
                    try:
                        # Convert date format if needed
                        dob = row['dob']
                        if isinstance(dob, pd.Timestamp):
                            dob = dob.strftime('%Y-%m-%d')
                        
                        # Call stored procedure to add student
                        result = db.call_procedure('sp_AddStudent', (
                            str(row['username']),
                            str(row['password']),
                            str(row['email']),
                            str(row['first_name']),
                            str(row['last_name']),
                            str(dob),
                            str(row['gender']),
                            str(row['phone']),
                            str(row['address']),
                            str(row['program']),
                            int(row['semester'])
                        ))
                        
                        if result:
                            success_count += 1
                        else:
                            error_count += 1
                            errors.append(f"Row {index + 2}: Failed to add student")
                    
                    except Exception as e:
                        error_count += 1
                        errors.append(f"Row {index + 2}: {str(e)}")
                
                # Remove uploaded file
                os.remove(filepath)
                
                # Display results
                if success_count > 0:
                    flash(f'Successfully added {success_count} student(s)', 'success')
                if error_count > 0:
                    flash(f'Failed to add {error_count} student(s)', 'error')
                    for error in errors[:5]:  # Show first 5 errors
                        flash(error, 'error')
                
                return redirect(url_for('admin_students'))
            
            except Exception as e:
                flash(f'Error processing file: {str(e)}', 'error')
                if os.path.exists(filepath):
                    os.remove(filepath)
                return redirect(request.url)
        else:
            flash('Invalid file type. Please upload .xlsx or .xls file', 'error')
            return redirect(request.url)
    
    return render_template('admin/upload_students.html')

@app.route('/admin/students/download-template')
def download_student_template():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    from flask import send_file
    from io import BytesIO
    
    # Create sample Excel template
    template_data = {
        'username': ['john.doe', 'jane.smith'],
        'password': ['password123', 'password456'],
        'email': ['john.doe@example.com', 'jane.smith@example.com'],
        'first_name': ['John', 'Jane'],
        'last_name': ['Doe', 'Smith'],
        'dob': ['2000-01-15', '2001-03-22'],
        'gender': ['Male', 'Female'],
        'phone': ['1234567890', '9876543210'],
        'address': ['123 Main St, City', '456 Oak Ave, Town'],
        'program': ['B.Tech CSE', 'B.Tech ECE'],
        'semester': [3, 5]
    }
    
    df = pd.DataFrame(template_data)
    
    # Create Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Students')
        
        # Auto-adjust column widths
        worksheet = writer.sheets['Students']
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    output.seek(0)
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='student_upload_template.xlsx'
    )

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
