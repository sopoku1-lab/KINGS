import sqlite3
from datetime import date

class DatabaseManager:
    def __init__(self, db_path="hr_system_new.db"):
        try:
            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise

    def execute(self, query, params=(), commit=False):
        try:
            self.cursor.execute(query, params)
            if commit:
                self.conn.commit()
            return self.cursor
        except sqlite3.Error as e:
            if commit:
                self.conn.rollback()
            print(f"SQL error: {e}")
            raise

    def fetchall(self):
        return self.cursor.fetchall()

    def close(self):
        if self.conn:
            self.conn.close()

class Employee:
    def __init__(self, db):
        self.db = db

    def view_training_history(self, employee_id):
        self.db.execute(
            """SELECT c.CourseName, c.Description, e.EnrollmentDate, e.CompletionDate, e.Score 
               FROM enrollments e 
               JOIN courses c ON e.CourseID = c.CourseID 
               WHERE e.EmployeeID = ?""",
            (employee_id,)
        )
        return self.db.fetchall()
        
    def enroll_in_course(self, employee_id, course_id):
        self.db.execute(
            """SELECT EnrollmentID FROM enrollments 
               WHERE EmployeeID = ? AND CourseID = ? AND CompletionDate IS NULL""", 
            (employee_id, course_id)
        )
        if self.db.cursor.fetchone():
            print("Error: Employee is already enrolled in this course")
            return False
            
        today = date.today()
        
        self.db.execute(
            "INSERT INTO enrollments (EmployeeID, CourseID, EnrollmentDate) VALUES (?, ?, ?)",
            (employee_id, course_id, today),
            commit=True
        )
        return True

class Course:
    def __init__(self, db):
        self.db = db

    def list_courses(self):
        self.db.execute("SELECT * FROM courses")
        return self.db.fetchall()

    def get_course(self, course_id):
        self.db.execute("SELECT * FROM courses WHERE CourseID = ?", (course_id,))
        return self.db.cursor.fetchone()

    def update_course(self, course_id, new_name=None, new_description=None, new_mandatory=None, new_start_date=None, new_end_date=None):
        course = self.get_course(course_id)
        if not course:
            print(f"Error: Course with ID {course_id} not found")
            return False

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
        if new_mandatory is not None:  
            self.db.execute(
                "UPDATE courses SET Mandatory = ? WHERE CourseID = ?",
                (new_mandatory, course_id),
                commit=True
            )
        if new_start_date:
            self.db.execute(
                "UPDATE courses SET StartDate = ? WHERE CourseID = ?",
                (new_start_date, course_id),
                commit=True
            )
        if new_end_date:
            self.db.execute(
                "UPDATE courses SET EndDate = ? WHERE CourseID = ?",
                (new_end_date, course_id),
                commit=True
            )
        return True

    def mark_course_completed(self, enrollment_id, score):
        self.db.execute(
            """SELECT e.EnrollmentID, e.CompletionDate, c.CourseID, c.CourseName, c.Description 
               FROM enrollments e
               JOIN courses c ON e.CourseID = c.CourseID
               WHERE e.EnrollmentID = ?""", 
            (enrollment_id,)
        )
        enrollment = self.db.cursor.fetchone()
        
        if not enrollment:
            print(f"Error: Enrollment with ID {enrollment_id} does not exist")
            return False, None
            
        if enrollment[1] is not None:
            print("Error: This course has already been marked as completed")
            return False, None
            
        if not 0 <= score <= 100:
            print("Error: Score must be between 0 and 100")
            return False, None
        
        today = date.today()
        self.db.execute(
            "UPDATE enrollments SET CompletionDate = ?, Score = ? WHERE EnrollmentID = ?",
            (today, score, enrollment_id),
            commit=True
        )
        
        course_info = {
            'id': enrollment[2],
            'name': enrollment[3],
            'description': enrollment[4]
        }
        
        return True, course_info
        
    def get_enrollment_with_course_info(self, enrollment_id):
        self.db.execute(
            """SELECT e.EnrollmentID, e.EmployeeID, e.CourseID, c.CourseName, c.Description, 
                      e.EnrollmentDate, e.CompletionDate, e.Score 
               FROM enrollments e
               JOIN courses c ON e.CourseID = c.CourseID
               WHERE e.EnrollmentID = ?""", 
            (enrollment_id,)
        )
        return self.db.cursor.fetchone()
        
    def list_incomplete_enrollments(self):
        self.db.execute(
            """SELECT e.EnrollmentID, emp.FirstName, emp.LastName, c.CourseName, c.Description, e.EnrollmentDate
               FROM enrollments e
               JOIN employees emp ON e.EmployeeID = emp.EmployeeID
               JOIN courses c ON e.CourseID = c.CourseID
               WHERE e.CompletionDate IS NULL
               ORDER BY e.EnrollmentDate"""
        )
        return self.db.fetchall()

def validate_date(date_str):
    """Simple date validation"""
    if not date_str:
        return None
        
    try:
        year, month, day = map(int, date_str.split('-'))
        return date(year, month, day)
    except ValueError:
        print("Error: Date must be in YYYY-MM-DD format")
        return None

def main():
    while True:
        try:
            db = DatabaseManager()
            employee = Employee(db)
            course = Course(db)

            print("\n--- HR Training App ---")
            print("Please select your role:")
            print("1. HR Manager")
            print("2. Employee")
            print("0. Exit Application")
            role_choice = input("Enter your choice: ")
            
            if role_choice == "1":
                hr_manager_menu(db, employee, course)
            elif role_choice == "2":
                try:
                    employee_id = int(input("Please enter your Employee ID: "))
                    employee_menu(db, employee, course, employee_id)
                except ValueError:
                    print("Error: Employee ID must be a number")
            elif role_choice == "0":
                print("Exiting application.")
                break
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if 'db' in locals():
                db.close()

def hr_manager_menu(db, employee, course):
    while True:
        print("\n--- HR Manager Menu ---")
        print("1. Update Course Details")
        print("2. View Employee Training History")
        print("3. Mark Course as Completed")
        print("0. Return to Main Menu")

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                print("\nAvailable Courses:")
                print("ID | Name | Description | Mandatory | Start Date | End Date")
                print("-" * 80)
                
                courses_list = course.list_courses()
                if not courses_list:
                    print("No courses available in the system.")
                    continue
                    
                for c in courses_list:
                    mandatory = "Yes" if c[3] == 1 else "No"
                    print(f"{c[0]} | {c[1]} | {c[2]} | {mandatory} | {c[4]} | {c[5]}")
                
                try:
                    cid = int(input("\nEnter Course ID to update (0 to cancel): "))
                    if cid == 0:
                        continue
                except ValueError:
                    print("Error: Course ID must be a number")
                    continue
                
                current_course = course.get_course(cid)
                if not current_course:
                    print(f"Error: Course with ID {cid} not found")
                    continue
                    
                print("\nCurrent Course Details:")
                print(f"ID: {current_course[0]}")
                print(f"Name: {current_course[1]}")
                print(f"Description: {current_course[2]}")
                print(f"Mandatory: {'Yes' if current_course[3] == 1 else 'No'}")
                print(f"Start Date: {current_course[4]}")
                print(f"End Date: {current_course[5]}")
                
                new_name = input("\nNew course name (or press enter to skip): ")
                new_desc = input("New description (or press enter to skip): ")
                
                new_mandatory = None
                new_mandatory_input = input("Is it mandatory? (1 for Yes, 0 for No, or press enter to skip): ")
                if new_mandatory_input:
                    try:
                        new_mandatory = int(new_mandatory_input)
                        if new_mandatory not in (0, 1):
                            print("Error: Mandatory field must be 0 or 1")
                            new_mandatory = None
                    except ValueError:
                        print("Error: Mandatory field must be a number")
                
                new_start = input("New start date (YYYY-MM-DD) (or press enter to skip): ")
                new_start_date = validate_date(new_start)
                
                new_end = input("New end date (YYYY-MM-DD) (or press enter to skip): ")
                new_end_date = validate_date(new_end)
                
                if course.update_course(
                    cid, 
                    new_name or None,
                    new_desc or None,
                    new_mandatory,
                    new_start_date,
                    new_end_date
                ):
                    print("Course updated successfully.")

            elif choice == "2":
                try:
                    eid = int(input("Employee ID (0 to cancel): "))
                    if eid == 0:
                        continue
                        
                    history = employee.view_training_history(eid)
                    if not history:
                        print("\nNo training history found for this employee.")
                    else:
                        print("\nTraining History for Employee ID:", eid)
                        print("Course Name | Description | Enrollment Date | Completion Date | Score")
                        print("-" * 90)
                        for record in history:
                            print(f"{record[0]} | {record[1]} | {record[2]} | {record[3] or 'Not completed'} | {record[4] or 'N/A'}")
                except ValueError:
                    print("Error: Employee ID must be a number")

            elif choice == "3":
                print("\nIncomplete Enrollments:")
                print("ID | Employee Name | Course Name | Description | Enrollment Date")
                print("-" * 90)
                
                incomplete = course.list_incomplete_enrollments()
                if not incomplete:
                    print("No incomplete enrollments found.")
                    continue
                    
                for inc in incomplete:
                    print(f"{inc[0]} | {inc[1]} {inc[2]} | {inc[3]} | {inc[4]} | {inc[5]}")
                
                try:
                    enrollment_id = int(input("\nEnter Enrollment ID to mark as completed (0 to cancel): "))
                    if enrollment_id == 0:
                        continue
                        
                    enrollment_info = course.get_enrollment_with_course_info(enrollment_id)
                    if not enrollment_info:
                        print(f"Error: Enrollment with ID {enrollment_id} not found")
                        continue
                        
                    if enrollment_info[6] is not None:  
                        print("This course has already been marked as completed")
                        continue
                        
                    print(f"\nMarking completion for: {enrollment_info[3]} - {enrollment_info[4]}")
                    print(f"Enrolled on: {enrollment_info[5]}")
                    
                    try:
                        score = int(input("Enter score (0-100): "))
                        success, course_info = course.mark_course_completed(enrollment_id, score)
                        if success:
                            print(f"Course '{course_info['name']}' marked as completed successfully.")
                    except ValueError:
                        print("Error: Score must be a number")
                except ValueError:
                    print("Error: Enrollment ID must be a number")

            elif choice == "0":
                print("Returning to main menu.")
                return
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")

def employee_menu(db, employee, course, employee_id):
    while True:
        print("\n--- Employee Menu ---")
        print("1. View Available Courses")
        print("2. Enroll in Course")
        print("0. Return to Main Menu")

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                courses_list = course.list_courses()
                if not courses_list:
                    print("\nNo courses available in the system.")
                    continue
                    
                print("\nAvailable Courses:")
                print("ID | Name | Description | Mandatory | Start Date | End Date")
                print("-" * 80)
                for c in courses_list:
                    mandatory = "Yes" if c[3] == 1 else "No"
                    print(f"{c[0]} | {c[1]} | {c[2]} | {mandatory} | {c[4]} | {c[5]}")

            elif choice == "2":
                courses_list = course.list_courses()
                if not courses_list:
                    print("\nNo courses available for enrollment.")
                    continue
                    
                print("\nAvailable Courses:")
                print("ID | Name | Description | Mandatory | Start Date | End Date")
                print("-" * 80)
                for c in courses_list:
                    mandatory = "Yes" if c[3] == 1 else "No"
                    print(f"{c[0]} | {c[1]} | {c[2]} | {mandatory} | {c[4]} | {c[5]}")
                
                try:
                    course_id = int(input("\nEnter Course ID to enroll (0 to cancel): "))
                    if course_id == 0:
                        continue
                    
                    course_details = course.get_course(course_id)
                    if not course_details:
                        print(f"Error: Course with ID {course_id} not found")
                        continue
                        
                    print(f"\nYou are enrolling in: {course_details[1]} - {course_details[2]}")
                    confirm = input("Confirm enrollment? (y/n): ").lower()
                    
                    if confirm == 'y':
                        if employee.enroll_in_course(employee_id, course_id):
                            print(f"Successfully enrolled in course: {course_details[1]}")
                    else:
                        print("Enrollment cancelled.")
                        
                except ValueError:
                    print("Error: Course ID must be a number")

            elif choice == "0":
                print("Returning to main menu.")
                return
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
    