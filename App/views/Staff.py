from flask import Blueprint, jsonify, request
from App.controllers import (
    create_staff, get_all_staff, get_staff, update_staff, delete_staff
)
from flask_jwt_extended import jwt_required

staff_views = Blueprint('staff_views', __name__)

# Create a new staff member
@staff_views.route('/staff', methods=['POST'])
#@jwt_required()  # Only admin users can create staff
def create_staff_action():
    data = request.json
    new_staff = create_staff(data['name'], data['position'], data['email'], data['department'])
    if new_staff:
        return jsonify({"message":f"{data['name']} was added to the staff!!!"}), 201
    return jsonify({"error": "Staff member with this email already exists."}), 409

# Get all staff members
@staff_views.route('/staff', methods=['GET'])
@jwt_required()
def get_all_staff_action():
    staff = get_all_staff()
    return jsonify(staff), 200

# Update a staff member's details
@staff_views.route('/staff/<int:staffID>', methods=['PUT'])
@jwt_required()
def update_staff_action(staffID):
    data = request.json
    updated_staff = update_staff(
        staffID, name=data.get('name'), position=data.get('position'),
        email=data.get('email'), department=data.get('department')
    )
    if updated_staff:
        return jsonify(updated_staff), 200
    return jsonify({'error': 'Staff member not found'}), 404

# Delete a staff member
@staff_views.route('/staff/<int:staffID>', methods=['DELETE'])
@jwt_required()  # Only admin users can delete staff
def delete_staff_action(staffID):
    success = delete_staff(staffID)
    if success:
        return jsonify({'message': 'Staff member deleted'}), 200
    return jsonify({'error': 'Staff member not found'}), 404
