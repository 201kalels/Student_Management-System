
import sqlite3


DATABASE_NAME = "students.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL,
            marks REAL NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_student(student):
    connection = get_connection()

    connection.execute("""
        INSERT INTO students (id, name, age, email, marks)
        VALUES (?, ?, ?, ?, ?)
    """, (
        student.id,
        student.name,
        student.age,
        student.email,
        student.marks
    ))

    connection.commit()
    connection.close()


def get_all_students():
    connection = get_connection()

    students = connection.execute("""
        SELECT id, name, age, email, marks
        FROM students
        ORDER BY id
    """).fetchall()

    connection.close()

    return [dict(student) for student in students]


def get_student_by_id(student_id):
    connection = get_connection()

    student = connection.execute("""
        SELECT id, name, age, email, marks
        FROM students
        WHERE id = ?
    """, (student_id,)).fetchone()

    connection.close()

    if student is None:
        return None

    return dict(student)


def delete_student(student_id):
    connection = get_connection()

    cursor = connection.execute("""
        DELETE FROM students
        WHERE id = ?
    """, (student_id,))

    connection.commit()

    deleted = cursor.rowcount > 0

    connection.close()

    return deleted
