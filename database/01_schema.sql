DROP DATABASE IF EXISTS student_management_system;
CREATE DATABASE student_management_system;
USE student_management_system;

CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'student', 'faculty') NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE,
    gender ENUM('Male', 'Female', 'Other'),
    phone VARCHAR(15),
    address TEXT,
    enrollment_date DATE NOT NULL,
    program VARCHAR(100),
    semester INT,
    status ENUM('Active', 'Inactive', 'Graduated') DEFAULT 'Active',
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Faculty (
    faculty_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    department VARCHAR(100),
    phone VARCHAR(15),
    email VARCHAR(100),
    qualification VARCHAR(100),
    hire_date DATE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_code VARCHAR(20) UNIQUE NOT NULL,
    course_name VARCHAR(100) NOT NULL,
    credits INT NOT NULL,
    department VARCHAR(100),
    semester INT,
    description TEXT
);

CREATE TABLE Course_Assignment (
    assignment_id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT,
    faculty_id INT,
    academic_year VARCHAR(20),
    semester INT,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE,
    FOREIGN KEY (faculty_id) REFERENCES Faculty(faculty_id) ON DELETE SET NULL
);

CREATE TABLE Enrollment (
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    course_id INT,
    enrollment_date DATE NOT NULL,
    academic_year VARCHAR(20),
    status ENUM('Enrolled', 'Dropped', 'Completed') DEFAULT 'Enrolled',
    FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE,
    UNIQUE KEY unique_enrollment (student_id, course_id, academic_year)
);

CREATE TABLE Attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    course_id INT,
    attendance_date DATE NOT NULL,
    status ENUM('Present', 'Absent', 'Late') NOT NULL,
    remarks TEXT,
    FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE
);

CREATE TABLE Grades (
    grade_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    course_id INT,
    assessment_type ENUM('Assignment', 'Midterm', 'Final', 'Quiz', 'Project') NOT NULL,
    marks_obtained DECIMAL(5,2),
    max_marks DECIMAL(5,2),
    grade_letter VARCHAR(2),
    academic_year VARCHAR(20),
    FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE
);

CREATE TABLE Fees (
    fee_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    academic_year VARCHAR(20),
    semester INT,
    total_amount DECIMAL(10,2) NOT NULL,
    paid_amount DECIMAL(10,2) DEFAULT 0,
    payment_date DATE,
    status ENUM('Pending', 'Partial', 'Paid') DEFAULT 'Pending',
    FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE
);

CREATE TABLE Announcements (
    announcement_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    posted_by INT,
    posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    target_audience ENUM('All', 'Students', 'Faculty') DEFAULT 'All',
    FOREIGN KEY (posted_by) REFERENCES Users(user_id) ON DELETE SET NULL
);

CREATE TABLE Timetable (
    timetable_id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT,
    faculty_id INT,
    day_of_week ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday') NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    room_number VARCHAR(20),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE,
    FOREIGN KEY (faculty_id) REFERENCES Faculty(faculty_id) ON DELETE SET NULL
);
