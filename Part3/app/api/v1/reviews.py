from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

# Data model for review validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
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
    @api.response(403, 'Forbidden')
    @api.response(404, 'Place not found')
    def post(self):
        """Register a new review"""
        review_data = api.payload
        current_user_id = get_jwt_identity()['id']

        try:
            # Validate the rating in the review data
            if 'rating' in review_data:
                validate_rating(review_data['rating'])

            # retrieving location information
            place = facade.get_place(review_data['place_id'])
            if not place:
                return {'error': 'Place not found'}, 404

            # Verification of the ownership of the place
            if place.owner_id == current_user_id:
                return {'error': 'You cannot review your own place'}, 403
            
            # verification of multiple assessments
            existing_review = facade.get_review_by_user_and_place(current_user_id, review_data['place_id'])
            if existing_review:
                return {'error': 'You have already reviewed this place'}, 400

            # Adding user_id to review_data:
            review_data['user_id'] = current_user_id

            # Create the new notice
            new_review = facade.create_review(review_data)
            return {
                "message": "Review successfully created",
                "data": new_review.to_dict()
            }, 201

        except ValueError as e:
            return {"error": str(e)}, 400

        except Exception as e:
            return {"error": "An unexpected error occurred."}, 500

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
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Forbidden')
    def put(self, review_id):
        """Update a review"""
        review_update = api.payload

        try:
            # Validate the rating in the review update data
            if 'rating' in review_update:
                validate_rating(review_update['rating'])

            # Retrieve the review
            review = facade.get_review(review_id)
            if not updated_review:
                return {"error": "Review not found"}, 404
            
            # Check review ownership
            current_user_id = get_jwt_identity()['id']
            if review.user_id != current_user_id:
                return {"error": "You are not authorized to update this review"}, 403

            # Update review
            updated_review = facade.update_review(review_id, review_update)

            return {
                "message": "Review updated successfully",
                "data": updated_review.to_dict()
            }, 200

        except ValueError as e:
            return {"error": str(e)}, 400

        except Exception as e:
            return {"error": "An unexpected error occurred."}, 500

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        try:
            if not facade.delete_review(review_id):
                return {"error": "Review not found"}, 404
            return {"message": "Review deleted successfully"}, 200

        except Exception as e:
            return {"error": "An unexpected error occurred."}, 500


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            place_reviews = facade.get_reviews_by_place(place_id)
            return {"data": [review.to_dict() for review in place_reviews]}, 200

        except Exception as e:
            return {"error": "An unexpected error occurred."}, 500
