USE student_management_system;

DELIMITER //

CREATE PROCEDURE sp_AddStudent(
    IN p_username VARCHAR(50),
    IN p_password VARCHAR(255),
    IN p_email VARCHAR(100),
    IN p_first_name VARCHAR(50),
    IN p_last_name VARCHAR(50),
    IN p_dob DATE,
    IN p_gender ENUM('Male', 'Female', 'Other'),
    IN p_phone VARCHAR(15),
    IN p_address TEXT,
    IN p_program VARCHAR(100),
    IN p_semester INT
)
BEGIN
    DECLARE v_user_id INT;
    
    INSERT INTO Users (username, password, role, email)
    VALUES (p_username, p_password, 'student', p_email);
    
    SET v_user_id = LAST_INSERT_ID();
    
    INSERT INTO Students (user_id, first_name, last_name, date_of_birth, gender, phone, address, enrollment_date, program, semester, status)
    VALUES (v_user_id, p_first_name, p_last_name, p_dob, p_gender, p_phone, p_address, CURDATE(), p_program, p_semester, 'Active');
END//

CREATE PROCEDURE sp_EnrollStudent(
    IN p_student_id INT,
    IN p_course_id INT,
    IN p_academic_year VARCHAR(20)
)
BEGIN
    INSERT INTO Enrollment (student_id, course_id, enrollment_date, academic_year, status)
    VALUES (p_student_id, p_course_id, CURDATE(), p_academic_year, 'Enrolled');
END//

CREATE PROCEDURE sp_MarkAttendance(
    IN p_student_id INT,
    IN p_course_id INT,
    IN p_date DATE,
    IN p_status ENUM('Present', 'Absent', 'Late')
)
BEGIN
    INSERT INTO Attendance (student_id, course_id, attendance_date, status)
    VALUES (p_student_id, p_course_id, p_date, p_status);
END//

CREATE PROCEDURE sp_AddGrade(
    IN p_student_id INT,
    IN p_course_id INT,
    IN p_assessment_type VARCHAR(50),
    IN p_marks_obtained DECIMAL(5,2),
    IN p_max_marks DECIMAL(5,2),
    IN p_academic_year VARCHAR(20)
)
BEGIN
    DECLARE v_grade_letter VARCHAR(2);
    DECLARE v_percentage DECIMAL(5,2);
    
    SET v_percentage = (p_marks_obtained / p_max_marks) * 100;
    
    SET v_grade_letter = CASE
        WHEN v_percentage >= 90 THEN 'A+'
        WHEN v_percentage >= 80 THEN 'A'
        WHEN v_percentage >= 70 THEN 'B+'
        WHEN v_percentage >= 60 THEN 'B'
        WHEN v_percentage >= 50 THEN 'C'
        ELSE 'F'
    END;
    
    INSERT INTO Grades (student_id, course_id, assessment_type, marks_obtained, max_marks, grade_letter, academic_year)
    VALUES (p_student_id, p_course_id, p_assessment_type, p_marks_obtained, p_max_marks, v_grade_letter, p_academic_year);
END//

CREATE PROCEDURE sp_GetStudentCourses(IN p_student_id INT)
BEGIN
    SELECT c.course_id, c.course_code, c.course_name, c.credits,
           f.first_name AS faculty_first_name, f.last_name AS faculty_last_name,
           e.status AS enrollment_status
    FROM Enrollment e
    JOIN Courses c ON e.course_id = c.course_id
    LEFT JOIN Course_Assignment ca ON c.course_id = ca.course_id
    LEFT JOIN Faculty f ON ca.faculty_id = f.faculty_id
    WHERE e.student_id = p_student_id AND e.status = 'Enrolled';
END//

CREATE PROCEDURE sp_GetAttendanceReport(
    IN p_student_id INT,
    IN p_course_id INT
)
BEGIN
    SELECT 
        COUNT(*) AS total_classes,
        SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) AS classes_attended,
        ROUND((SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS attendance_percentage
    FROM Attendance
    WHERE student_id = p_student_id AND course_id = p_course_id;
END//

CREATE FUNCTION fn_CalculateGPA(p_student_id INT, p_academic_year VARCHAR(20))
RETURNS DECIMAL(3,2)
DETERMINISTIC
BEGIN
    DECLARE v_gpa DECIMAL(3,2);
    
    SELECT AVG(
        CASE grade_letter
            WHEN 'A+' THEN 4.0
            WHEN 'A' THEN 3.7
            WHEN 'B+' THEN 3.3
            WHEN 'B' THEN 3.0
            WHEN 'C' THEN 2.0
            ELSE 0.0
        END
    ) INTO v_gpa
    FROM Grades
    WHERE student_id = p_student_id AND academic_year = p_academic_year;
    
    RETURN IFNULL(v_gpa, 0.0);
END//

CREATE TRIGGER tr_UpdateFeeStatus
BEFORE UPDATE ON Fees
FOR EACH ROW
BEGIN
    IF NEW.paid_amount >= NEW.total_amount THEN
        SET NEW.status = 'Paid';
    ELSEIF NEW.paid_amount > 0 THEN
        SET NEW.status = 'Partial';
    ELSE
        SET NEW.status = 'Pending';
    END IF;
END//

DELIMITER ;
