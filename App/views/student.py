from flask import Blueprint, render_template, jsonify, request
from flask_jwt_extended import jwt_required

from.index import index_views

from App.controllers import (
    create_student,
    get_student,
    get_all_students,
    update_student,
    delete_student,
    jwt_required
)

student_views = Blueprint('student_views', __name__)

# Create a new student
@student_views.route('/students', methods=['POST'])
@jwt_required()  # Only staff or admin users can create students
def create_student_action():
    data = request.json
    new_student = create_student(data['name'], data['year'], data['program'])
    return jsonify(new_student.get_json()), 201

# Get all students
@student_views.route('/students', methods=['GET'])
@jwt_required()
def get_all_students_action():
    students = get_all_students()
    return jsonify(students), 200

# Get a student by ID
@student_views.route('/students/<int:studentID>', methods=['GET'])
@jwt_required()
def get_student_action(studentID):
    student = get_student(studentID)
    if student:
        return jsonify(student), 200
    return jsonify({'error': 'Student not found'}), 404

# Update a student's details
@student_views.route('/students/<int:studentID>', methods=['PUT'])
@jwt_required()
def update_student_action(studentID):
    data = request.json
    updated_student = update_student(
        studentID, name=data.get('name'), year=data.get('year'), program=data.get('program')
    )
    if updated_student:
        return jsonify(updated_student), 200
    return jsonify({'error': 'Student not found'}), 404

# Delete a student
@student_views.route('/students/<int:studentID>', methods=['DELETE'])
@jwt_required()
def delete_student_action(studentID):
    success = delete_student(studentID)
    if success:
        return jsonify({'message': 'Student deleted'}), 200
    return jsonify({'error': 'Student not found'}), 404


