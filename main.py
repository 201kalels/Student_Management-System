import sqlite3
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
app=FastAPI()
DB="students.db"
class Student(BaseModel):
    id:int
    name: str = Field(min_length=2)
    age: int = Field(ge=5, le=100)
    email: EmailStr
    marks: float = Field(default=0, ge=0, le=100)
#dbconnect and table creation by setup function
def setup_db():
    with sqlite3.connect(DB)as conn:
        conn.execute("""create table if not exists students(id,INTEGER PRIMARY KEY,name TEXT NOT NULL,
        age INTEGER NOT NULL,email TEXT NOT NULL,
        marks REAL NOT NULL CHECK(marks>=0 AND marks<=100))""")
setup_db()

@app.post("/students",status_code=201)
def add_student(students:Student):
    try:
       conn.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?)",
                (student.id, student.name, student.age,
                 str(student.email), student.marks))
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Student ID already exists")
    return {"message": "Student added", "student": student}

@app.get("/students")
def get_students():
    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM students ORDER BY id").fetchall()
    return [dict(row) for row in rows]

@app.get("/students/{student_id}")
def get_student(student_id: int):
    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM students WHERE id = ?",
                           (student_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return dict(row)

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted"}
