#Part2/app/api/v1/reviews.py
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        review_data = api.payload

        try:
            # Validate the rating in the review data
            if 'rating' in review_data:
                validate_rating(review_data['rating'])

            new_review = facade.create_review(review_data)
            return {
                "message": "Review successfully created",
                "id": new_review.id,
                "data": new_review.to_dict()
            }, 201

        except ValueError as e:
            return {"error": str(e)}, 400

        except Exception as e:
            return {"error": "An unexpected error occurred."}, 500

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        all_reviews = facade.get_all_reviews()
        return [{'id': review.id, 'text': review.text, 'rating': review.rating,
                 'user_id': review.user_id, 'place_id': review.place_id} for review in all_reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {'id': review.id, 'text': review.text, 'rating': review.rating,
                'user_id': review.user_id, 'place_id': review.place_id}, 200

    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        review_data = api.payload
        updated_review = facade.update_review(review_id, review_data)
        if not updated_review:
            return {'error': 'Review not found'}, 404
        return {'id': updated_review.id, 'text': updated_review.text, 'rating': updated_review.rating,
                'user_id': updated_review.user_id, 'place_id': updated_review.place_id}, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review by ID"""
        deleted_review = facade.delete_review(review_id)
        if not deleted_review:
            return {'error': 'Review not found'}, 404
        return {"message": "Review deleted successfully"}, 200

def validate_rating(rating):
    """Validate that the rating is between 1 and 5."""
    if not (1 <= rating <= 5):
        raise ValueError("Rating must be between 1 and 5")
