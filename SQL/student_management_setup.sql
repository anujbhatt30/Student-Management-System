CREATE DATABASE student_management;
SHOW DATABASES;
USE Student_management;

CREATE TABLE Student(
student_id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(50) NOT NULL,
age INT NOT NULL,
gender ENUM ('Male','Female','Others') NOT NULL,
city VARCHAR(100)
);

DESC Student;    -- --To Check Feild,Type,Null,Key 

SELECT * FROM Student;

INSERT INTO Student(name, age, gender, city)
VALUES
('Anuj',21,'Male','Etawah'),
('Rohan',22,'Male','Goa'),
('Priya',20,'Female','Delhi'),
('Amit',23,'Male','Lucknow'),
('Neha',21,'Female','Kanpur'),
('Rahul',22,'Male','Agra'),
('Sneha',20,'Female','Noida'),
('Vikas',24,'Male','Jaipur'),
('Pooja',21,'Female','Mumbai'),
('Arjun',22,'Male','Pune'),
('Karan',23,'Male','Chandigarh'),
('Simran',20,'Female','Amritsar'),
('Ayesha',21,'Female','Hyderabad'),
('Nikhil',22,'Male','Bhopal'),
('Ritika',20,'Female','Indore');


SELECT * FROM Student;


CREATE TABLE Course(
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(100) NOT NULL
);

INSERT INTO Course(course_name)
VALUES
('Python'),
('SQL'),
('Data Science'),
('Machine Learning'),
('Statistics'),
('Power BI');

SELECT * FROM Course;



CREATE TABLE Enrollment(
enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
student_id INT NOT NULL,
course_id INT NOT NULL,

UNIQUE(student_id, course_id), -- 

FOREIGN KEY (student_id)
REFERENCES Student(student_id),

FOREIGN KEY (course_id)
REFERENCES Course(course_id)
);

SHOW TABLES;
DESC Enrollment;

INSERT INTO Enrollment(student_id, course_id)
VALUES
(1,1),(1,2),
(2,2),(2,3),
(3,1),(3,4),
(4,2),(4,5),
(5,3),(5,6),
(6,1),(6,2),
(7,4),(7,5),
(8,2),(8,6),
(9,1),(9,3),
(10,5),(10,6),
(11,2),(11,4),
(12,1),(12,5),
(13,3),(13,6),
(14,2),(14,4),
(15,1),(15,3);

SELECT * FROM Enrollment;


CREATE TABLE Marks(
student_id int,
course_id int,
semester INT CHECK (semester BETWEEN 1 AND 8), -- using check to limit the values  

assignment_marks INT CHECK (assignment_marks BETWEEN 0 AND 20),
midterm_marks INT CHECK (midterm_marks BETWEEN 0 AND 30),
finalterm_marks INT CHECK (finalterm_marks BETWEEN 0 AND 50),

PRIMARY KEY(student_id , course_id,semester), -- uniquely identifies a record/marks can be stored separately for each semester

FOREIGN KEY (student_id)
references Student(student_id),      

FOREIGN KEY (course_id)
REFERENCES Course(course_id)  

);

INSERT INTO Marks
(student_id, course_id, semester,
 assignment_marks, midterm_marks, finalterm_marks)
VALUES

(1,1,1,18,25,42),
(1,2,1,19,28,45),

(2,2,1,15,22,38),
(2,3,1,17,25,40),

(3,1,1,20,29,48),
(3,4,2,18,27,44),

(4,2,1,14,20,35),
(4,5,2,16,24,39),

(5,3,2,19,28,46),
(5,6,2,18,26,43),

(6,1,1,12,18,30),
(6,2,1,13,21,34),

(7,4,2,17,25,41),
(7,5,2,15,23,38),

(8,2,1,20,29,47),
(8,6,2,18,27,45),

(9,1,1,14,22,36),
(9,3,2,16,24,40),

(10,5,2,17,26,42),
(10,6,2,19,28,46),

(11,2,1,13,19,33),
(11,4,2,15,22,37),

(12,1,1,20,30,49),
(12,5,2,19,28,47),

(13,3,2,16,25,40),
(13,6,2,18,27,43),

(14,2,1,14,20,35),
(14,4,2,15,23,38),

(15,1,1,19,29,46),
(15,3,2,18,28,45);

SELECT * FROM Marks;


