import sqlite3
from datetime import date

def populate_hr_database(db_name="hr_system_new.db"):
    """
    Populates the HR database with sample employees and courses only.
    No enrollment data is created so you can enroll employees manually.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # --- Insert 10 employees ---
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
        INSERT INTO employees (FirstName, LastName, Email, Department, HireDate)
        VALUES (?, ?, ?, ?, ?)
        """,
        employees
    )

    # --- Insert course data ---
    courses = [
        ("Python Basics", "Introduction to Python programming", 1, date(2024, 1, 1), date(2024, 12, 31)),
        ("Data Science Essentials", "Fundamental concepts of data science", 0, date(2024, 2, 15), date(2024, 12, 15)),
        ("HR Compliance Training", "Overview of HR laws and regulations", 1, date(2024, 3, 1), date(2024, 12, 15)),
        ("Management Skills", "Techniques for effective management", 0, date(2024, 4, 1), date(2024, 12, 30)),
        ("Cybersecurity Awareness", "Best practices for online safety", 1, date(2024, 5, 1), date(2024, 12, 15)),
    ]
    cursor.executemany(
        """
        INSERT INTO courses (CourseName, Description, Mandatory, StartDate, EndDate)
        VALUES (?, ?, ?, ?, ?)
        """,
        courses
    )

    conn.commit()
    conn.close()
    print("Sample employees and courses inserted successfully.")
    print("No enrollment data was created - you can enroll employees manually through your application.")

if __name__ == "__main__":
    populate_hr_database()