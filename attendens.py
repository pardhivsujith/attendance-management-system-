import sqlite3
from datetime import date

# Connect to database (creates file if not exists)
conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    date TEXT,
    status TEXT,
    FOREIGN KEY(student_id) REFERENCES students(id)
)
""")

conn.commit()

# Add student
def add_student():
    name = input("Enter student name: ")
    cursor.execute("INSERT INTO students (name) VALUES (?)", (name,))
    conn.commit()
    print("✅ Student added successfully!")

# View students
def view_students():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    print("\n📋 Student List:")
    for s in students:
        print(f"ID: {s[0]}, Name: {s[1]}")

# Mark attendance
def mark_attendance():
    view_students()
    student_id = int(input("Enter student ID: "))
    status = input("Enter status (P/A): ").upper()

    today = str(date.today())

    if status == "P":
        status_full = "Present"
    else:
        status_full = "Absent"

    cursor.execute("""
    INSERT INTO attendance (student_id, date, status)
    VALUES (?, ?, ?)
    """, (student_id, today, status_full))

    conn.commit()
    print("✅ Attendance marked!")

# View attendance
def view_attendance():
    cursor.execute("""
    SELECT students.name, attendance.date, attendance.status
    FROM attendance
    JOIN students ON students.id = attendance.student_id
    """)
    
    records = cursor.fetchall()
    
    print("\n📊 Attendance Records:")
    for r in records:
        print(f"Name: {r[0]}, Date: {r[1]}, Status: {r[2]}")

# Menu system
while True:
    print("\n====== Attendance Management System ======")
    print("1. Add Student")
    print("2. View Students")
    print("3. Mark Attendance")
    print("4. View Attendance")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_student()
    elif choice == "2":
        view_students()
    elif choice == "3":
        mark_attendance()
    elif choice == "4":
        view_attendance()
    elif choice == "5":
        print("Exiting...")
        break
    else:
        print("❌ Invalid choice!")

# Close connection
conn.close()