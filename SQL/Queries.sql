-- 1: Display Students and Their Enrolled Courses:-
SELECT 
    s.student_id, s.name, c.course_name
FROM
    Student S
        JOIN
    Enrollment E ON s.student_id = e.student_id
        JOIN
    Course C ON e.course_id = c.course_id;



-- Query 2: Student Report Card:-
SELECT 
    s.student_id,
    s.name,
    c.course_name,
    m.semester,
    m.assignment_marks,
    m.midterm_marks,
    m.finalterm_marks,
    (m.assignment_marks + m.midterm_marks + m.finalterm_marks) AS TotalMarks
FROM
    Student S
        JOIN
    Marks M ON s.student_id = m.student_id
        JOIN
    Course C ON m.course_id = c.course_id;
       





-- 3: Top 5 Students Based on Average Marks:-
SELECT 
    s.student_id,
    s.name,
    AVG(m.assignment_marks + m.midterm_marks + m.finalterm_marks) AS AverageMarks
FROM
    Student S
        JOIN
    marks m ON s.student_id = m.student_id
GROUP BY s.student_id , s.name
ORDER BY AverageMarks DESC
LIMIT 5;
       
       
       
    
       
-- 4: Course-wise Average Marks:-
SELECT 
    c.course_id,
    c.course_name,
    AVG(assignment_marks + midterm_marks + finalterm_marks) AS AverageMarks
FROM
    Course C
        INNER JOIN
    marks m ON c.course_id = m.course_id
GROUP BY c.course_id , c.course_name
ORDER BY AverageMarks DESC;      
       
       
       
       

       
       
-- 5: Grade Calculation A,B,C:-
SELECT 
    s.student_id,
    s.name,
    c.course_name,
    (assignment_marks + midterm_marks + finalterm_marks) AS TotalMarks, -- CASE is a conditional statement in SQL used to implement if-else logic. 
    CASE
        WHEN (assignment_marks + midterm_marks + finalterm_marks) >= 90 THEN 'A'
        WHEN (assignment_marks + midterm_marks + finalterm_marks) >= 75 THEN 'B'
        WHEN (assignment_marks + midterm_marks + finalterm_marks) >= 60 THEN 'C'
        ELSE 'D'
    END AS Grade
FROM
    Student S
        JOIN
    marks m ON s.student_id = m.student_id
        JOIN
    course c ON m.course_id = c.course_id;
       
       
       
-- 6: Students Scoring Above 90:-
SELECT 
    s.student_id,
    s.name,
    c.course_name,
    (m.assignment_marks + midterm_marks + finalterm_marks) AS TotalMarks
FROM
    Student S
        JOIN
    Marks M ON s.student_id = m.student_id
        JOIN
    Course C ON m.course_id = c.course_id
WHERE
    (m.assignment_marks + midterm_marks + finalterm_marks) >= 90; -- WHERE filters individual rows before grouping. Since we are checking each student's total marks record, WHERE is appropriate 
       
       
       
       
-- 7: Number of Students in Each Course:-
SELECT 
    c.course_name, COUNT(e.student_id) TotalStudent -- COUNT() is an aggregate function used to count the number of rows in a group 
FROM
    Course C
        JOIN
    enrollment e ON c.course_id = e.course_id
GROUP BY c.course_name
ORDER BY TotalStudent DESC;   

 
 


-- 8: Highest Scoring Student:--- 
SELECT 
    s.student_id,
    s.name,
    MAX(m.assignment_marks + midterm_marks + finalterm_marks) AS HighestMarks -- MAX() is an aggregate function that returns the largest value in a group 
FROM
    Student S
        JOIN
    Marks M ON s.student_id = m.student_id
GROUP BY s.student_id , s.name
ORDER BY HighestMarks DESC
LIMIT 1;


-- 9: Display the course names where the number of enrolled students is greater than the average number of students enrolled across all courses.
SELECT 
    c.course_name, COUNT(e.enrollment_id) AS Student_count
FROM
    enrollment e
        JOIN
    course c ON e.course_id = c.course_id
GROUP BY c.course_name , c.course_name
HAVING COUNT(e.enrollment_id) > (SELECT 
        AVG(Total)
    FROM
        (SELECT 
            COUNT(enrollment_id) AS Total
        FROM
            enrollment
        GROUP BY course_id) t);



       