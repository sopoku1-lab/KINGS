import sqlite3
from datetime import date, timedelta
import random

def populate_hr_database(db_name="hr_system.db"):
    """
    Populates the HR database with sample data, including at least 10 employees.

    Args:
        db_name (str, optional): The name of the SQLite database file.
            Defaults to "hr_system.db".
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # --- Insert sample data into the employees table ---
    employees = [
        ("Alice", "Smith", "alice.smith@example.com", "Engineering", date(2020, 1, 15)),
        ("Bob", "Johnson", "bob.johnson@example.com", "Marketing", date(2021, 3, 10)),
        ("Charlie", "Brown", "charlie.brown@example.com", "Sales", date(2019, 11, 1)),
        ("Diana", "Miller", "diana.miller@example.com", "HR", date(2022, 5, 20)),
        ("Ethan", "Davis", "ethan.davis@example.com", "Finance", date(2020, 8, 5)),
        ("Fiona", "Wilson", "fiona.wilson@example.com", "Engineering", date(2023, 2, 28)),
        ("George", "Garcia", "george.garcia@example.com", "Marketing", date(2021, 7, 12)),
        ("Hannah", "Rodriguez", "hannah.rodriguez@example.com", "Sales", date(2018, 9, 23)),
        ("Isaac", "Williams", "isaac.williams@example.com", "HR", date(2022, 12, 1)),
        ("Jessica", "Brown", "jessica.brown@example.com", "Finance", date(2024, 1, 18)),
    ]
    cursor.executemany(
        """
        INSERT INTO employees (FirstName, LastName, Emails, Departments, HireDate)
        VALUES (?, ?, ?, ?, ?)
        """,
        employees,
    )

    # --- Insert sample data into the courses table ---
    courses = [
        ("Python Basics", "Introduction to Python programming", 1, date(2024, 1, 1), date(2024, 1, 31)),
        ("Data Science Essentials", "Fundamental concepts of data science", 0, date(2024, 2, 15), date(2024, 3, 15)),
        ("HR Compliance Training", "Overview of HR laws and regulations", 1, date(2024, 3, 1), date(2024, 3, 15)),
        ("Management Skills", "Techniques for effective management", 0, date(2024, 4, 1), date(2024, 4, 30)),
        ("Cybersecurity Awareness", "Best practices for online safety", 1, date(2024, 5, 1), date(2024, 5, 15)),
    ]
    cursor.executemany(
        """
        INSERT INTO courses (CourseName, Description, Mandatory, StartDate, EndDate)
        VALUES (?, ?, ?, ?, ?)
        """,
        courses,
    )

    # --- Insert sample data into the hr_manager table ---
    hr_managers = [
        ("Jane", "Doe", "jane.doe@example.com", "555-1234"),
        ("John", "Smith", "john.smith@example.com", "555-5678"),
    ]
    cursor.executemany(
        """
        INSERT INTO hr_manager (FirstName, LastName, Email, Phone)
        VALUES (?, ?, ?, ?)
        """,
        hr_managers,
    )

    # --- Insert sample data into the reports table ---
    reports = [
        (1, "Employee Performance Report", date(2024, 2, 1)),
        (1, "Training Progress Report", date(2024, 3, 1)),
        (2, "Hiring Report", date(2024, 4, 1)),
    ]
    cursor.executemany(
        """
        INSERT INTO reports (ManagerID, ReportName, ReportDate)
        VALUES (?, ?, ?)
        """,
        reports,
    )

    # --- Insert sample data into the enrollments table ---
    # Create some enrollment data.  Make sure the EmployeeIDs and CourseIDs
    # exist in the Employees and Courses tables.  The ReportIDs must
    # exist in the Reports table.
    enrollments = []

    # Enroll each employee in a couple of courses, and assign them to a report.
    for employee_id in range(1, len(employees) + 1):
        # Enroll in Python Basics (CourseID 1) and HR Compliance (CourseID 3)
        enrollments.append((employee_id, 1, 1, date(2024, 1, 10), date(2024, 1, 30), random.randint(70, 100)))
        enrollments.append((employee_id, 3, 2, date(2024, 3, 5), date(2024, 3, 14), random.randint(80, 100)))
    cursor.executemany(
        """
        INSERT INTO enrollments (EmployeeID, CourseID, ReportID, EnrollmentDate, CompletionDate, Score)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        enrollments,
    )

    conn.commit()
    conn.close()
    print("Sample data inserted successfully.")


if __name__ == "__main__":
    populate_hr_database()
