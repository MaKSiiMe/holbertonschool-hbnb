from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model(
    'Review', {
        'text': fields.String(required=True, description='Text of the review'),
        'rating': fields.Integer(required=True,
                                 description='Rating of the place (1-5)'),
        'place_id': fields.String(required=True, description='ID of the place')
    }
)

updated_review_model = api.model(
    'UpdatedReview', {
        'text': fields.String(description='Update th text of the review'),
        'rating': fields.Integer(
            description='Update the rating of the place (1-5)'
            ),
    }
)


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.doc(security="token")
    @jwt_required()
    def post(self):
        """Register a new review"""
        current_user = get_jwt_identity()
        review_data = api.payload
        try:

            place = facade.get_place(review_data['place_id'])
            review_data['user_id'] = current_user['id']
            if place.owner_id == current_user:
                return {'message': 'You cannot review your own place'}, 400

            current_user_id = current_user['id']
            existing_review = facade.get_review_by_user_and_place(
                current_user_id, review_data['place_id']
                )
            if existing_review:
                return {'message': 'You already reviewed this place'}, 400

            required_fields = {'text', 'rating', 'user_id', 'place_id'}
            if not required_fields.issubset(review_data):
                return {'message': 'Missing required fields'}, 400

            new_review = facade.create_review(review_data)

            return {
                'id': new_review.id,
                'message': 'Review succesfully created'
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except TypeError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
            }
            for review in reviews
        ], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review with ID"""
        try:
            review = facade.get_review(review_id)
            if not review:
                return {'error': 'Review not found'}, 404

            return {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.expect(updated_review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.doc(security="token")
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        review_data = api.payload
        current_user = get_jwt_identity()
        review_data['user_id'] = current_user['id']

        review = facade.get_review(review_id)

        if review.user_id != current_user['id']:
            return {'error': 'Unauthorized action'}, 403
        try:
            if not review:
                return {'error': 'Review not found'}, 404

            new_review = facade.update_review(review_id, review_data)
            return {
                'id': new_review.id,
                'message': 'Review succesfully updated'
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except TypeError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.doc(security="token")
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        review = facade.get_review(review_id)
        current_user = get_jwt_identity()
        if review.user_id != current_user['id']:
            return {'error': 'Unauthorized action'}, 403
        try:
            review = facade.delete_review(review_id)
            if review:
                return {'message': 'Review deleted.'}, 200
            return {'error': 'Review not found'}, 404
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            place_reviews = facade.get_reviews_by_place(place_id)
            return [
                {
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating
                }
                for review in place_reviews
            ], 200
        except ValueError as e:
            return {'error': str(e)}, 400
