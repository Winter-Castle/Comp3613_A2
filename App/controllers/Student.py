from App.models import Student, Review
from App.database import db

# Create a new student
def create_student(name, year, program, email):
    new_student = Student(name=name, year=year, program=program, email=email)
    existing_student = Student.query.filter_by(email=email).first()

    if not existing_student:
        db.session.add(new_student)
        db.session.commit()
        return new_student
    return None

# Get a student by studentID
def get_student(studentID):
    student = Student.query.get(studentID)
    if student:
        return student.get_json()
    return None

# Get all students
def get_all_students():
    students = Student.query.all()
    return [student.get_json() for student in students]

# Update a student by studentID
def update_student(studentID, name=None, year=None, program=None, email=None):
    student = Student.query.get(studentID)
    if student:
        if name:
            student.name = name
        if year:
            student.year = year
        if program:
            student.program = program
        if email:
            student.email = email
        db.session.commit()
        return student.get_json()
    return None

# Delete a student by studentID
def delete_student(studentID):
    student = Student.query.get(studentID)
    if student:
        db.session.delete(student)
        db.session.commit()
        return True
    return False


