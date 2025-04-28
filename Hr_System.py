import sqlite3
from datetime import date

class DatabaseManager:
    def __init__(self, db_path="hr_system.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def execute(self, query, params=(), commit=False):
        self.cursor.execute(query, params)
        if commit:
            self.conn.commit()
        return self.cursor

    def fetchall(self):
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

class Employee:
    def __init__(self, db):
        self.db = db

    def add_employee(self, first_name, last_name, email, department, hire_date):
        self.db.execute(
            "INSERT INTO employees (FirstName, LastName, Emails, Departments, HireDate) VALUES (?, ?, ?, ?, ?)",
            (first_name, last_name, email, department, hire_date),
            commit=True
        )

    def view_training_history(self, employee_id):
        self.db.execute(
            """SELECT c.CourseName, e.EnrollmentDate, e.Score 
               FROM enrollments e 
               JOIN courses c ON e.CourseID = c.CourseID 
               WHERE e.EmployeeID = ?""",
            (employee_id,)
        )
        return self.db.fetchall()
        
    def enroll_in_course(self, employee_id, course_id):
        today = date.today()
        
        self.db.execute("SELECT ReportID FROM reports LIMIT 1")
        report = self.db.cursor.fetchone()
        
        if not report:
            self.db.execute(
                "INSERT INTO reports (ManagerID, ReportName, ReportDate) VALUES (?, ?, ?)",
                (1, "Default Employee Self-Enrollment Report", today),
                commit=True
            )
            self.db.execute("SELECT last_insert_rowid()")
            report_id = self.db.cursor.fetchone()[0]
        else:
            report_id = report[0]
        
        self.db.execute(
            "INSERT INTO enrollments (EmployeeID, CourseID, ReportID, EnrollmentDate) VALUES (?, ?, ?, ?)",
            (employee_id, course_id, report_id, today),
            commit=True
        )
        
    def complete_training(self, enrollment_id, score):
        today = date.today()
        self.db.execute(
            "UPDATE enrollments SET CompletionDate = ?, Score = ? WHERE EnrollmentID = ?",
            (today, score, enrollment_id),
            commit=True
        )

class Course:
    def __init__(self, db):
        self.db = db

    def list_courses(self):
        self.db.execute("SELECT * FROM courses")
        return self.db.fetchall()

    def add_course(self, name, description, mandatory, start_date, end_date):
        self.db.execute(
            "INSERT INTO courses (CourseName, Description, Mandatory, StartDate, EndDate) VALUES (?, ?, ?, ?, ?)",
            (name, description, mandatory, start_date, end_date),
            commit=True
        )

    def update_course(self, course_id, new_name=None, new_description=None):
        if new_name:
            self.db.execute(
                "UPDATE courses SET CourseName = ? WHERE CourseID = ?",
                (new_name, course_id),
                commit=True
            )
        if new_description:
            self.db.execute(
                "UPDATE courses SET Description = ? WHERE CourseID = ?",
                (new_description, course_id),
                commit=True
            )

class Report:
    def __init__(self, db):
        self.db = db

    def create_report(self, manager_id, name):
        today = date.today()
        self.db.execute(
            "INSERT INTO reports (ManagerID, ReportName, ReportDate) VALUES (?, ?, ?)",
            (manager_id, name, today),
            commit=True
        )

    def delete_report(self, report_id):
        self.db.execute(
            "DELETE FROM reports WHERE ReportID = ?",
            (report_id,),
            commit=True
        )
        
    def list_reports(self):
        self.db.execute(
            """SELECT r.ReportID, r.ReportName, r.ReportDate, e.FirstName, e.LastName
               FROM reports r
               JOIN employees e ON r.ManagerID = e.EmployeeID"""
        )
        return self.db.fetchall()

class HRManager:
    def __init__(self, db):
        self.db = db

    def view_incomplete_mandatory_trainings(self):
        self.db.execute(
            """
            SELECT e.EmployeeID, e.FirstName, e.LastName, c.CourseName 
            FROM enrollments en
            JOIN employees e ON en.EmployeeID = e.EmployeeID
            JOIN courses c ON en.CourseID = c.CourseID
            WHERE c.Mandatory = 1 AND en.CompletionDate IS NULL
            """
        )
        return self.db.fetchall()

def main():
    while True:
        db = DatabaseManager()
        employee = Employee(db)
        course = Course(db)
        report = Report(db)
        hr_manager = HRManager(db)

        print("\n--- HR Training App ---")
        print("Please select your role:")
        print("1. HR Manager")
        print("2. Employee")
        print("0. Exit Application")
        role_choice = input("Enter your choice: ")
        
        if role_choice == "1":
            hr_manager_menu(db, employee, course, report, hr_manager)
            db.close()
        elif role_choice == "2":
            try:
                employee_id = int(input("Please enter your Employee ID: "))
                employee_menu(db, employee, course, employee_id)
            except ValueError:
                print("Invalid Employee ID. Please enter a number.")
            db.close()
        elif role_choice == "0":
            print("Exiting application.")
            db.close()
            break
        else:
            print("Invalid choice. Try again.")
            db.close()

def hr_manager_menu(db, employee, course, report, hr_manager):
    while True:
        print("\n--- HR Manager Menu ---")
        print("1. Add New Employee")
        print("2. Add New Course")
        print("3. Update Course Details")
        print("4. View All Courses")
        print("5. View Employee Training History")
        print("6. View All Reports")
        print("7. Delete Report")
        print("8. View Incomplete Mandatory Trainings")
        print("0. Return to Main Menu")

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                fname = input("First name: ")
                lname = input("Last name: ")
                email = input("Email: ")
                dept = input("Department: ")
                hdate = input("Hire Date (YYYY-MM-DD): ")
                employee.add_employee(fname, lname, email, dept, hdate)
                print("Employee added.")

            elif choice == "2":
                cname = input("Course name: ")
                desc = input("Description: ")
                mandatory = int(input("Is it mandatory? (1 for Yes, 0 for No): "))
                sdate = input("Start date (YYYY-MM-DD): ")
                edate = input("End date (YYYY-MM-DD): ")
                course.add_course(cname, desc, mandatory, sdate, edate)
                print("Course added.")

            elif choice == "3":
                cid = int(input("Course ID to update: "))
                new_name = input("New course name (or press enter to skip): ")
                new_desc = input("New description (or press enter to skip): ")
                course.update_course(cid, new_name or None, new_desc or None)
                print("Course updated.")

            elif choice == "4":
                print("\nAll Courses:")
                for c in course.list_courses():
                    print(c)

            elif choice == "5":
                eid = int(input("Employee ID: "))
                history = employee.view_training_history(eid)
                print("\nTraining History:")
                for record in history:
                    print(record)

            elif choice == "6":
                print("\nAll Reports:")
                for r in report.list_reports():
                    print(r)

            elif choice == "7":
                rid = int(input("Report ID to delete: "))
                report.delete_report(rid)
                print("Report deleted.")

            elif choice == "8":
                alerts = hr_manager.view_incomplete_mandatory_trainings()
                print("\nIncomplete Mandatory Trainings:")
                for alert in alerts:
                    print(alert)

            elif choice == "0":
                print("Returning to main menu.")
                return
            else:
                print("Invalid choice. Try again.")

        except Exception as e:
            print(f"Error occurred: {e}")

def employee_menu(db, employee, course, employee_id):
    while True:
        print("\n--- Employee Menu ---")
        print("1. View Available Courses")
        print("2. Enroll in Course")
        print("3. Mark Course as Completed")
        print("4. View My Training History")
        print("0. Return to Main Menu")

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                print("\nAvailable Courses:")
                for c in course.list_courses():
                    print(c)

            elif choice == "2":
                course_id = int(input("Enter Course ID to enroll: "))
                employee.enroll_in_course(employee_id, course_id)
                print("Successfully enrolled in course.")

            elif choice == "3":
                enrollment_id = int(input("Enter Enrollment ID to mark as completed: "))
                score = int(input("Enter your score: "))
                employee.complete_training(enrollment_id, score)
                print("Training marked as completed.")

            elif choice == "4":
                history = employee.view_training_history(employee_id)
                print("\nYour Training History:")
                for record in history:
                    print(record)

            elif choice == "0":
                print("Returning to main menu.")
                return
            else:
                print("Invalid choice. Try again.")

        except Exception as e:
            print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()