from flask import Blueprint, jsonify, request
from App.controllers import (
    create_review, get_review, get_all_reviews, get_reviews_by_category,
    get_reviews_for_student, get_reviews_by_staff, update_review, delete_review
)
from flask_jwt_extended import jwt_required, get_jwt_identity

review_views = Blueprint('review_views', __name__)

# Create a new review (Staff must be logged in)
@review_views.route('/reviews', methods=['POST'])
@jwt_required()  # Only staff users can create reviews
def create_review_action():
    data = request.json
    current_user = get_jwt_identity()  # Get the ID of the logged-in user (staff)
    new_review = create_review(
        review_type=data['review_type'],
        comment=data['comment'],
        date=data['date'],
        review_status=data['review_status'],
        category=data['category'],
        studentID=data['studentID'],
        staffID=current_user  # Assuming staffID = userID from token
    )
    return jsonify(new_review.get_json()), 201

# Get a specific review by its ID
@review_views.route('/reviews/<int:reviewID>', methods=['GET'])
@jwt_required()
def get_review_action(reviewID):
    review = get_review(reviewID)
    if review:
        return jsonify(review), 200
    return jsonify({'error': 'Review not found'}), 404

# Get all reviews
@review_views.route('/reviews', methods=['GET'])
@jwt_required()
def get_all_reviews_action():
    reviews = get_all_reviews()
    return jsonify(reviews), 200

# Get reviews filtered by category
@review_views.route('/reviews/category/<string:category>', methods=['GET'])
@jwt_required()
def get_reviews_by_category_action(category):
    reviews = get_reviews_by_category(category)
    return jsonify(reviews), 200

# Get reviews for a specific student
@review_views.route('/reviews/student/<int:studentID>', methods=['GET'])
@jwt_required()
def get_reviews_for_student_action(studentID):
    reviews = get_reviews_for_student(studentID)
    return jsonify(reviews), 200

# Get reviews by a specific staff member
@review_views.route('/reviews/staff/<int:staffID>', methods=['GET'])
@jwt_required()
def get_reviews_by_staff_action(staffID):
    reviews = get_reviews_by_staff(staffID)
    return jsonify(reviews), 200

# Update a review
@review_views.route('/reviews/<int:reviewID>', methods=['PUT'])
@jwt_required()  # Staff members only
def update_review_action(reviewID):
    data = request.json
    updated_review = update_review(
        reviewID,
        review_type=data.get('review_type'),
        comment=data.get('comment'),
        review_status=data.get('review_status'),
        category=data.get('category')
    )
    if updated_review:
        return jsonify(updated_review), 200
    return jsonify({'error': 'Review not found'}), 404

# Delete a review
@review_views.route('/reviews/<int:reviewID>', methods=['DELETE'])
@jwt_required()  # Staff members only
def delete_review_action(reviewID):
    success = delete_review(reviewID)
    if success:
        return jsonify({'message': 'Review deleted'}), 200
    return jsonify({'error': 'Review not found'}), 404