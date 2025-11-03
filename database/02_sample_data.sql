USE student_management_system;

INSERT INTO Users (username, password, role, email) VALUES
('admin', 'admin123', 'admin', 'admin@university.edu'),
('john.student', 'pass123', 'student', 'john.student@university.edu'),
('sarah.student', 'pass123', 'student', 'sarah.student@university.edu'),
('mike.student', 'pass123', 'student', 'mike.student@university.edu'),
('emma.student', 'pass123', 'student', 'emma.student@university.edu'),
('dr.smith', 'faculty123', 'faculty', 'dr.smith@university.edu'),
('dr.johnson', 'faculty123', 'faculty', 'dr.johnson@university.edu'),
('prof.williams', 'faculty123', 'faculty', 'prof.williams@university.edu');

INSERT INTO Students (user_id, first_name, last_name, date_of_birth, gender, phone, address, enrollment_date, program, semester, status) VALUES
(2, 'John', 'Doe', '2003-05-15', 'Male', '9876543210', '123 Main St, Mumbai', '2023-08-01', 'Computer Science', 3, 'Active'),
(3, 'Sarah', 'Williams', '2003-08-22', 'Female', '9876543211', '456 Park Ave, Delhi', '2023-08-01', 'Computer Science', 3, 'Active'),
(4, 'Mike', 'Brown', '2004-01-10', 'Male', '9876543212', '789 Lake Rd, Bangalore', '2024-08-01', 'Information Technology', 1, 'Active'),
(5, 'Emma', 'Davis', '2003-11-30', 'Female', '9876543213', '321 Hill St, Pune', '2023-08-01', 'Computer Science', 3, 'Active');

INSERT INTO Faculty (user_id, first_name, last_name, department, phone, email, qualification, hire_date) VALUES
(6, 'Robert', 'Smith', 'Computer Science', '9988776655', 'dr.smith@university.edu', 'PhD in Computer Science', '2015-07-01'),
(7, 'Lisa', 'Johnson', 'Computer Science', '9988776656', 'dr.johnson@university.edu', 'PhD in Data Science', '2017-08-15'),
(8, 'David', 'Williams', 'Information Technology', '9988776657', 'prof.williams@university.edu', 'M.Tech in IT', '2018-09-01');

INSERT INTO Courses (course_code, course_name, credits, department, semester, description) VALUES
('CS101', 'Programming Fundamentals', 4, 'Computer Science', 1, 'Introduction to programming concepts'),
('CS201', 'Data Structures', 4, 'Computer Science', 2, 'Study of data structures and algorithms'),
('CS301', 'Database Management Systems', 3, 'Computer Science', 3, 'Database design and SQL'),
('CS302', 'Operating Systems', 3, 'Computer Science', 3, 'OS concepts and design'),
('IT101', 'Web Technologies', 3, 'Information Technology', 1, 'HTML, CSS, JavaScript basics'),
('IT201', 'Network Security', 3, 'Information Technology', 2, 'Network security fundamentals');

INSERT INTO Course_Assignment (course_id, faculty_id, academic_year, semester) VALUES
(1, 1, '2024-25', 1),
(2, 1, '2024-25', 2),
(3, 2, '2024-25', 3),
(4, 2, '2024-25', 3),
(5, 3, '2024-25', 1),
(6, 3, '2024-25', 2);

INSERT INTO Enrollment (student_id, course_id, enrollment_date, academic_year, status) VALUES
(1, 3, '2024-08-01', '2024-25', 'Enrolled'),
(1, 4, '2024-08-01', '2024-25', 'Enrolled'),
(2, 3, '2024-08-01', '2024-25', 'Enrolled'),
(2, 4, '2024-08-01', '2024-25', 'Enrolled'),
(3, 1, '2024-08-01', '2024-25', 'Enrolled'),
(3, 5, '2024-08-01', '2024-25', 'Enrolled'),
(4, 3, '2024-08-01', '2024-25', 'Enrolled'),
(4, 4, '2024-08-01', '2024-25', 'Enrolled');

INSERT INTO Attendance (student_id, course_id, attendance_date, status) VALUES
(1, 3, '2024-11-01', 'Present'),
(1, 3, '2024-11-02', 'Present'),
(1, 4, '2024-11-01', 'Absent'),
(2, 3, '2024-11-01', 'Present'),
(2, 4, '2024-11-01', 'Present'),
(3, 1, '2024-11-01', 'Late'),
(4, 3, '2024-11-01', 'Present');

INSERT INTO Grades (student_id, course_id, assessment_type, marks_obtained, max_marks, grade_letter, academic_year) VALUES
(1, 3, 'Midterm', 85, 100, 'A', '2024-25'),
(1, 4, 'Midterm', 78, 100, 'B+', '2024-25'),
(2, 3, 'Midterm', 92, 100, 'A+', '2024-25'),
(2, 4, 'Midterm', 88, 100, 'A', '2024-25'),
(3, 1, 'Quiz', 45, 50, 'A', '2024-25'),
(4, 3, 'Assignment', 38, 40, 'A', '2024-25');

INSERT INTO Fees (student_id, academic_year, semester, total_amount, paid_amount, payment_date, status) VALUES
(1, '2024-25', 3, 50000, 50000, '2024-08-15', 'Paid'),
(2, '2024-25', 3, 50000, 25000, '2024-08-15', 'Partial'),
(3, '2024-25', 1, 45000, 45000, '2024-08-20', 'Paid'),
(4, '2024-25', 3, 50000, 0, NULL, 'Pending');

INSERT INTO Announcements (title, content, posted_by, target_audience) VALUES
('Mid-Semester Exams', 'Mid-semester exams will be held from Nov 15-20, 2024', 1, 'Students'),
('Faculty Meeting', 'Monthly faculty meeting scheduled for Nov 10, 2024', 1, 'Faculty'),
('Holiday Notice', 'University will remain closed on Nov 5, 2024', 1, 'All');

INSERT INTO Timetable (course_id, faculty_id, day_of_week, start_time, end_time, room_number) VALUES
(3, 2, 'Monday', '09:00:00', '10:30:00', 'CS-101'),
(4, 2, 'Tuesday', '11:00:00', '12:30:00', 'CS-102'),
(1, 1, 'Wednesday', '09:00:00', '10:30:00', 'CS-103'),
(5, 3, 'Thursday', '14:00:00', '15:30:00', 'IT-201');
