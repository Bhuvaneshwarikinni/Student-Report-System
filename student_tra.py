# ==========================================
# STUDENT PERFORMANCE TRACKER PROJECT
# ==========================================

import sqlite3

# Database Connection
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    roll TEXT PRIMARY KEY,
    name TEXT,
    math INTEGER,
    science INTEGER,
    english INTEGER,
    total INTEGER,
    percentage REAL,
    grade TEXT
)
''')
conn.commit()

# List to store records temporarily
students = []

# Function to calculate grade
def calculate_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "Fail"

# Function to add student
def add_student():
    print("\n===== Add Student Record =====")

    name = input("Enter Student Name: ")
    roll = input("Enter Roll Number: ")

    math = int(input("Enter Math Marks: "))
    science = int(input("Enter Science Marks: "))
    english = int(input("Enter English Marks: "))

    total = math + science + english
    percentage = total / 3
    grade = calculate_grade(percentage)

    # Save to database
    try:
        cursor.execute("""
        INSERT INTO students VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (roll, name, math, science, english, total, percentage, grade))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Roll Number already exists!")
        return

    # Save to text file
    with open("student_report.txt", "a") as file:
        file.write(f"{name}, {roll}, {math}, {science}, {english}, {total}, {percentage:.2f}, {grade}\n")

    # Save to list
    student = {
        "Name": name,
        "Roll": roll,
        "Math": math,
        "Science": science,
        "English": english,
        "Total": total,
        "Percentage": percentage,
        "Grade": grade
    }

    students.append(student)

    print("\nStudent Record Added Successfully!")
    print(f"Total Marks: {total}")
    print(f"Percentage: {percentage:.2f}%")
    print(f"Grade: {grade}\n")

# Function to display all records
def display_students():
    print("\n===== All Student Records =====")

    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()

    if not records:
        print("No records found.\n")
        return

    for student in records:
        print("-----------------------------------")
        print("Roll Number  :", student[0])
        print("Student Name :", student[1])
        print("Math Marks   :", student[2])
        print("Science Marks:", student[3])
        print("English Marks:", student[4])
        print("Total Marks  :", student[5])
        print("Percentage   : {:.2f}%".format(student[6]))
        print("Grade        :", student[7])
        print("-----------------------------------")

# Function to search student
def search_student():
    print("\n===== Search Student =====")

    roll = input("Enter Roll Number to Search: ")

    cursor.execute("SELECT * FROM students WHERE roll = ?", (roll,))
    student = cursor.fetchone()

    if student:
        print("\nStudent Found!")
        print("-----------------------------------")
        print("Roll Number  :", student[0])
        print("Student Name :", student[1])
        print("Math Marks   :", student[2])
        print("Science Marks:", student[3])
        print("English Marks:", student[4])
        print("Total Marks  :", student[5])
        print("Percentage   : {:.2f}%".format(student[6]))
        print("Grade        :", student[7])
        print("-----------------------------------")
    else:
        print("Student record not found.\n")

# Main menu
def main():
    while True:
        print("""
==========================================
     STUDENT PERFORMANCE TRACKER
==========================================
1. Add Student Record
2. Display All Student Records
3. Search Student by Roll Number
4. Exit
==========================================
""")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            add_student()
        elif choice == "2":
            display_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            print("\nThank you for using Student Performance Tracker!")
            conn.close()
            break
        else:
            print("\nInvalid choice! Please enter a number between 1 and 4.\n")

# Run Program
main()