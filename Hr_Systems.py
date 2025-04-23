from datetime import date

class HRManager:
    def __init__(self, manager_id, first_name, last_name, email, phone):
        self.manager_id = manager_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone

    def view_report(self, reports):
        return [r for r in reports if r.manager_id == self.manager_id]

    def view_course(self, courses):
        return [c for c in courses if c.manager_id == self.manager_id]

    def view_training_history(self, enrollments, employee_id):
        return [e for e in enrollments if e.employee_id == employee_id]


class Employee:
    def __init__(self, employee_id, first_name, last_name, email, department, hire_date):
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.department = department
        self.hire_date = hire_date

    def register(self):
        print(f"{self.first_name} {self.last_name} registered successfully.")

    def view_courses(self, courses):
        for course in courses:
            print(f"{course.course_name} - Mandatory: {course.mandatory}")

    def view_history(self, enrollments):
        return [e for e in enrollments if e.employee_id == self.employee_id]


class Course:
    def __init__(self, course_id, course_name, description, mandatory, start_date, end_date, manager_id):
        self.course_id = course_id
        self.course_name = course_name
        self.description = description
        self.mandatory = mandatory
        self.start_date = start_date
        self.end_date = end_date
        self.manager_id = manager_id

    def add_course(self):
        print(f"Course {self.course_name} added successfully.")

    def update_course(self, name=None, desc=None):
        if name:
            self.course_name = name
        if desc:
            self.description = desc
        print(f"Course {self.course_id} updated successfully.")


class Enrollment:
    def __init__(self, enrollment_id, employee_id, course_id, enrollment_date, completion_date=None, score=None):
        self.enrollment_id = enrollment_id
        self.employee_id = employee_id
        self.course_id = course_id
        self.enrollment_date = enrollment_date
        self.completion_date = completion_date
        self.score = score

    def enroll(self):
        print(f"Employee {self.employee_id} enrolled in course {self.course_id}.")

    def update_score(self, score):
        self.score = score
        print(f"Score for enrollment {self.enrollment_id} updated to {self.score}.")


class Report:
    def __init__(self, report_id, report_name, report_date, manager_id):
        self.report_id = report_id
        self.report_name = report_name
        self.report_date = report_date
        self.manager_id = manager_id

    def create_report(self):
        print(f"Report {self.report_name} created.")

    def delete_report(self):
        print(f"Report {self.report_name} deleted.")



