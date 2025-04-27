import sqlite3

def create_hr_database(db_name="hr_system.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create Employees table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        EmployeeID INTEGER PRIMARY KEY AUTOINCREMENT,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,
        Emails TEXT NOT NULL,
        Departments TEXT NOT NULL,
        HireDate DATE NOT NULL
    )
    """)

    # Create Courses table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        CourseID INTEGER PRIMARY KEY AUTOINCREMENT,
        CourseName TEXT NOT NULL,
        Description TEXT,
        Mandatory BOOLEAN NOT NULL DEFAULT 0,
        StartDate DATE,
        EndDate DATE
    )
    """)

    # Create HR_Manager table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hr_manager (
        ManagerID INTEGER PRIMARY KEY AUTOINCREMENT,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,
        Email TEXT NOT NULL,
        Phone TEXT
    )
    """)

    # Create Reports table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        ReportID INTEGER PRIMARY KEY AUTOINCREMENT,
        ManagerID INTEGER NOT NULL,
        ReportName TEXT NOT NULL,
        ReportDate DATE NOT NULL DEFAULT CURRENT_DATE,
        FOREIGN KEY (ManagerID) REFERENCES hr_manager (ManagerID)
    )
    """)

    # Create Enrollments table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS enrollments (
        EnrollmentID INTEGER PRIMARY KEY AUTOINCREMENT,
        EmployeeID INTEGER NOT NULL,
        CourseID INTEGER NOT NULL,
        ReportID INTEGER NOT NULL,
        EnrollmentDate DATE NOT NULL DEFAULT CURRENT_DATE,
        CompletionDate DATE,
        Score INTEGER,
        FOREIGN KEY (EmployeeID) REFERENCES employees (EmployeeID),
        FOREIGN KEY (CourseID) REFERENCES courses (CourseID),
        FOREIGN KEY (ReportID) REFERENCES reports (ReportID)
    )
    """)

    conn.commit()
    conn.close()
    print(f"Database '{db_name}' created successfully.")

if __name__ == "__main__":
    create_hr_database()
