# abwelcome30062004

import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="abwelcome30062004",
    database="student_management"
)

cursor = conn.cursor()
while True:
    try:

        print("\n===== STUDENT MANAGEMENT SYSTEM =====")
        print("1. View Students")
        print("2. View Courses")
        print("3. Search Student")
        print("4. Add Student")
        print("5. Update Student")
        print("6. Delete Student")
        print("7. Student Course Report")
        print("8. Exit")
        
        choice = int(input("Enter Choice: "))

        if choice not in range(1, 9):
            print("Please enter a number between 1 and 8.")
            continue

        # VIEW STUDENTS
        if choice == 1:

            cursor.execute("SELECT * FROM Student")

            students = cursor.fetchall()

            print("\n===== STUDENT LIST =====\n")

            for student in students:
                print(student)

        # VIEW COURSES
        elif choice == 2:

            cursor.execute("SELECT * FROM Course")

            courses = cursor.fetchall()

            print("\n===== COURSE LIST =====\n")

            for course in courses:
                print(course)

        # SEARCH STUDENT
        elif choice == 3:

            student_id = int(input("Enter Student ID Here: "))

            cursor.execute(
                "SELECT * FROM Student WHERE student_id=%s",
                (student_id,)
            )

            student = cursor.fetchone()

            if student:

                print("\n===== STUDENT FOUND =====")

                print("ID:", student[0])
                print("Name:", student[1])
                print("Age:", student[2])
                print("Gender:", student[3])
                print("City:", student[4])

            else:
                print("Student Not Found!")

        # ADD STUDENT
        elif choice == 4:

            try:    
                name = input("Enter Name Here: ")
                age = int(input("Enter Age Here: "))
                gender = input("Enter Gender Here: ")
                city = input("Enter City Here: ")

                cursor.execute("""
                INSERT INTO Student(name, age, gender, city)
                VALUES (%s, %s, %s, %s)
                """, (name, age, gender, city))

                student_id = cursor.lastrowid

                print("\nAvailable Courses:")
                cursor.execute("SELECT * FROM Course")

                for course in cursor.fetchall():
                    print(course)

                course_id = int(input("Enter Course ID Here: "))

                cursor.execute("""
                INSERT INTO Enrollment(student_id, course_id)
                VALUES (%s, %s)
                """, (student_id, course_id))

                semester = int(input("Enter Semester Here: "))
                assignment = int(input("Enter Assignment Marks Here: "))
                midterm = int(input("Enter Midterm Marks Here: "))
                finalterm = int(input("Enter Finalterm Marks Here: "))

                cursor.execute("""
                INSERT INTO Marks(
                    student_id,
                    course_id,
                    semester,
                    assignment_marks,
                    midterm_marks,
                    finalterm_marks
                )
                VALUES (%s,%s,%s,%s,%s,%s)
                """,
                (
                    student_id,
                    course_id,
                    semester,
                    assignment,
                    midterm,
                    finalterm
                ))

                conn.commit()

                print("Student Added Successfully!")
                print("Generated Student ID:", student_id)

            except mysql.connector.Error as err:
                conn.rollback()
                print("Database Error:", err)

                # UPDATE STUDENT
        elif choice == 5:

                    student_id = int(input("Enter Student ID Here: "))

                    cursor.execute(
                        "SELECT * FROM Student WHERE student_id=%s",
                        (student_id,)
                    )

                    student = cursor.fetchone()

                    if not student:
                        print("Student Not Found!")
                        continue

                    new_name = input("Enter New Name Here: ")
                    new_city = input("Enter New City Here: ")

                    cursor.execute("""
                    UPDATE Student
                    SET name=%s,
                        city=%s
                    WHERE student_id=%s
                    """,
                    (
                        new_name,
                        new_city,
                        student_id
                    ))

                    conn.commit()

                    print("Student Updated Successfully!")

        # DELETE STUDENT
        elif choice == 6:
            try:

                student_id = int(input("Enter Student ID To Delete: "))

                cursor.execute(
                "SELECT * FROM Student WHERE student_id=%s",
                (student_id,)
            )

                student = cursor.fetchone()

                if not student:
                    print("Student Not Found!")
                    continue

                cursor.execute("""
                DELETE FROM Marks
                WHERE student_id=%s
                """, (student_id,))

                cursor.execute("""
                DELETE FROM Enrollment
                WHERE student_id=%s
                """, (student_id,))

                cursor.execute("""
                DELETE FROM Student
                WHERE student_id=%s
                """, (student_id,))

                conn.commit()

                print("Student Deleted Successfully!")

            except mysql.connector.Error as err:
                conn.rollback()
                print("Database Error:", err)


            # STUDENT COURSE REPORT
        elif choice == 7:
            

                cursor.execute("""
                    SELECT
                    s.student_id,
                    s.name,
                    c.course_name,
                    m.semester,
                    m.assignment_marks,
                    m.midterm_marks,
                    m.finalterm_marks,
                    (
                        m.assignment_marks +
                        m.midterm_marks +
                        m.finalterm_marks
                    ) AS total_marks

                FROM Student s

                JOIN Enrollment e
                    ON s.student_id = e.student_id

                JOIN Course c
                    ON e.course_id = c.course_id

                JOIN Marks m
                    ON s.student_id = m.student_id
                    AND c.course_id = m.course_id
                """)

                report = cursor.fetchall()

                print("\n===== STUDENT COURSE REPORT =====")

                for row in report:

                    print(f"""
                ID: {row[0]}
                Name: {row[1]}
                Course: {row[2]}
                Semester: {row[3]}
                Assignment Marks: {row[4]}
                Midterm Marks: {row[5]}
                Finalterm Marks: {row[6]}
                Total Marks: {row[7]}
                -----------------------------------
                """)

        # EXIT
        elif choice == 8:

            print("Thank You!")
            break

        else:
            print("Invalid Choice!")

    except ValueError:
        print("Please enter numbers only!")

    except mysql.connector.Error as err:
        print("Database Error:", err)

    except Exception as e:
        print("Unexpected Error:", e)

cursor.close()
conn.close()
