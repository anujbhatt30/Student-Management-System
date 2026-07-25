from tkinter import ttk
import mysql.connector
import tkinter as tk

root = tk.Tk()
root.title("Student Management System")
root.geometry("900x600")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="abwelcome30062004",
    database="student_management"
)

cursor = conn.cursor()

# Heading
heading = tk.Label(
    root,
    text="STUDENT MANAGEMENT SYSTEM",
    font=("Arial", 20, "bold")
)
heading.pack(pady=10)

# Left Frame (Buttons/Menu)
left_frame = tk.Frame(root, bd=2, relief="solid")
left_frame.pack(side="left", fill="y", padx=10, pady=10)

# Right Frame (Content Area)
right_frame = tk.Frame(root, bd=2, relief="solid")
right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# Treeview
tree = ttk.Treeview(
    right_frame,
    columns=("ID", "Name", "Age", "Gender", "City"),
    show="headings"
)

tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.heading("Gender", text="Gender")
tree.heading("City", text="City")

tree.pack(fill="both", expand=True)


from tkinter import messagebox

def add_student_window():

        window = tk.Toplevel(root)
        window.title("Add Student")
        window.geometry("400x500")

        tk.Label(window, text="Name").pack()
        name_entry = tk.Entry(window)
        name_entry.pack()

        tk.Label(window, text="Age").pack()
        age_entry = tk.Entry(window)
        age_entry.pack()

        tk.Label(window, text="Gender").pack()
        gender_entry = tk.Entry(window)
        gender_entry.pack()

        tk.Label(window, text="City").pack()
        city_entry = tk.Entry(window)
        city_entry.pack()

        tk.Label(window, text="Course ID").pack()
        course_entry = tk.Entry(window)
        course_entry.pack()

        tk.Label(window, text="Semester").pack()
        sem_entry = tk.Entry(window)
        sem_entry.pack()

        tk.Label(window, text="Assignment Marks").pack()
        assignment_entry = tk.Entry(window)
        assignment_entry.pack()

        tk.Label(window, text="Midterm Marks").pack()
        midterm_entry = tk.Entry(window)
        midterm_entry.pack()

        tk.Label(window, text="Finalterm Marks").pack()
        finalterm_entry = tk.Entry(window)
        finalterm_entry.pack()

        def save_student():

            name = name_entry.get()
            age = int(age_entry.get())
            gender = gender_entry.get()
            city = city_entry.get()

            course_id = int(course_entry.get())
            semester = int(sem_entry.get())

            assignment = int(assignment_entry.get())
            midterm = int(midterm_entry.get())
            finalterm = int(finalterm_entry.get())

            cursor.execute("""
            INSERT INTO Student(name, age, gender, city)
            VALUES (%s,%s,%s,%s)
            """, (name, age, gender, city))

            student_id = cursor.lastrowid

            cursor.execute("""
            INSERT INTO Enrollment(student_id, course_id)
            VALUES (%s,%s)
            """, (student_id, course_id))

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
            """, (
                student_id,
                course_id,
                semester,
                assignment,
                midterm,
                finalterm
            ))
            try:
                conn.commit()

                messagebox.showinfo(
                    "Success",
                    "Student Added Successfully!"
                )

                window.destroy()
            except mysql.connector.Error as err:
                conn.rollback()
                messagebox.showerror(
                "Database Error",
                str(err)
                )

        view_students()
        tk.Button(
        window,
        text="Save Student",
        command=save_student
        ).pack(pady=10)

def update_student_window():

    selected = tree.focus()

    if not selected:
        messagebox.showerror(
            "Error",
            "Please select a student first."
        )
        return

    data = tree.item(selected)["values"]

    student_id = data[0]

    window = tk.Toplevel(root)
    window.title("Update Student")
    window.geometry("300x250")

    tk.Label(window, text="Name").pack()

    name_entry = tk.Entry(window)
    name_entry.insert(0, data[1])
    name_entry.pack()

    tk.Label(window, text="City").pack()

    city_entry = tk.Entry(window)
    city_entry.insert(0, data[4])
    city_entry.pack()

    def save_update():

        new_name = name_entry.get()
        new_city = city_entry.get()

        try:

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

            messagebox.showinfo(
                "Success",
                "Student Updated Successfully!"
            )

            window.destroy()

            view_students()

        except mysql.connector.Error as err:

            conn.rollback()

            messagebox.showerror(
                "Database Error",
                str(err)
            )

    tk.Button(
        window,
        text="Update",
        command=save_update
    ).pack(pady=10)        
        

def delete_student():

    selected = tree.focus()

    if not selected:
        messagebox.showerror(
            "Error",
            "Please select a student first."
        )
        return

    data = tree.item(selected)["values"]

    student_id = data[0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Delete Student ID {student_id} ?"
    )

    if not confirm:
        return

    try:

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

        messagebox.showinfo(
            "Success",
            "Student Deleted Successfully!"
        )

        view_students()

    except mysql.connector.Error as err:

        conn.rollback()

        messagebox.showerror(
            "Database Error",
            str(err)
        )



def student_report():

    for row in tree.get_children():
        tree.delete(row)

    # Change tree columns for report
    tree["columns"] = (
        "ID",
        "Name",
        "Course",
        "Semester",
        "Assignment",
        "Midterm",
        "Finalterm",
        "Total"
    )

    tree["show"] = "headings"

    headings = [
        "ID",
        "Name",
        "Course",
        "Semester",
        "Assignment",
        "Midterm",
        "Finalterm",
        "Total"
    ]

    for col in headings:
        tree.heading(col, text=col)
        tree.column(col, width=100)

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

    for row in report:
        tree.insert("", "end", values=row)

# Buttons
btn_add = tk.Button(
    left_frame,
    text="Add Student",
    width=20,
    command=add_student_window
)
btn_add.pack(pady=5)

btn_update = tk.Button(
    left_frame,
    text="Update Student",
    width=20,
    command=update_student_window
)
btn_update.pack(pady=5)

btn_delete = tk.Button(
    left_frame,
    text="Delete Student",
    width=20,
    command=delete_student
)
btn_delete.pack(pady=5)

btn_report = tk.Button(
    left_frame,
    text="Student Report",
    width=20,
    command=student_report
)
btn_report.pack(pady=5)


def view_students():

    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM Student")

    students = cursor.fetchall()

    for student in students:
        tree.insert("", "end", values=student)


btn_view = tk.Button(
    left_frame,
    text="View Students",
    width=20,
    command=view_students
)
btn_view.pack(pady=5)

def on_closing():
    cursor.close()
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

view_students()
root.mainloop()