#app/api/v1/reviews.py

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

def validate_rating(rating):
    """Validate that the rating is between 1 and 5."""
    if not (1 <= rating <= 5):
        raise ValueError("Rating must be between 1 and 5")

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        current_user = get_jwt_identity()
        review_data = api.payload
        try:
            place_id = review_data['place_id']
            place = facade.get_place(place_id)
            if not place:
                return {"error": "Place not found"}, 404
            if place.owner_id == current_user:
                return {"error": "You cannot review your own place."}, 400
            if facade.has_reviewed_place(current_user, place_id):
                return {"error": "You have already reviewed this place."}, 400
            validate_rating(review_data['rating'])
            review_data['user_id'] = current_user
            new_review = facade.create_review(review_data)
            return {
                "message": "Review successfully created",
                "data": new_review.to_dict()
            }, 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        try:
            reviews = facade.get_all_reviews()
            return {"data": [review.to_dict() for review in reviews]}, 200
        except Exception as e:
            return {"error": "An unexpected error occurred."}, 500

@api.route('/<review_id>')
class ReviewResource(Resource):
    @jwt_required()
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return {"data": review.to_dict()}, 200

    @jwt_required()
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review"""
        current_user = get_jwt()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')
        review_update = api.payload
        try:
            review = facade.get_review(review_id)
            if not review:
                return {"error": "Review not found"}, 404
            if not is_admin and review.user_id != user_id:
                return {"error": "Unauthorized action"}, 403
            validate_rating(review_update['rating'])
            updated_review = facade.update_review(review_id, review_update, user_id=user_id)
            return {
                "message": "Review updated successfully",
                "data": updated_review.to_dict()
            }, 200
        except ValueError as e:
            return {"error": str(e)}, 400

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')
        try:
            review = facade.get_review(review_id)
            if not review:
                return {"error": "Review not found"}, 404
            if not is_admin and review.user_id != user_id:
                return {"error": "Unauthorized action"}, 403
            facade.delete_review(review_id, user_id=user_id)
            return {"message": "Review deleted successfully"}, 200
        except Exception as e:
            return {"error": "An unexpected error occurred."}, 500
