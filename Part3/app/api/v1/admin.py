#app/api/v1/admin.py

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('admin', description='Admin-only operations')

user_model = api.model('AdminUser', {
    'first_name': fields.String(description='User first name'),
    'last_name': fields.String(description='User last name'),
    'email': fields.String(description='User email (must be unique)'),
    'password': fields.String(description='User password (min 8 chars)'),
    'is_admin': fields.Boolean(description='Is the user an admin?')
})

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(description='Detailed description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Geographic latitude'),
    'longitude': fields.Float(required=True, description='Geographic longitude'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description='List of amenity IDs')
})

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

def is_admin(user_id):
    user = facade.get_user_by_id(user_id)
    return user.is_admin if user else False

@api.route('/users')
class AdminUserList(Resource):
    @jwt_required()
    @api.response(200, 'Users retrieved successfully')
    @api.response(403, 'Unauthorized action')
    def get(self):
        """Retrieve all users (admin-only)."""
        current_user = get_jwt_identity()
        if not is_admin(current_user):
            return {'error': 'Unauthorized action'}, 403
        users = facade.get_all_users()
        return [{'id': user.id, 
                 'first_name': user.first_name,
                 'last_name': user.last_name,
                 'email': user.email,
                 'is_admin': user.is_admin} for user in users], 200

    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'User created successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new user (admin-only)."""
        current_user = get_jwt_identity()
        if not is_admin(current_user):
            return {'error': 'Unauthorized action'}, 403
        user_data = api.payload
        try:
            new_user = facade.create_user(user_data)
            return {
                'message': 'User created successfully',
                'data': {
                    'id': new_user.id,
                    'first_name': new_user.first_name,
                    'last_name': new_user.last_name,
                    'email': new_user.email,
                    'is_admin': new_user.is_admin
                }
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

@api.route('/users/<user_id>')
class AdminUserResource(Resource):
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Modify any user's details (admin-only)."""
        current_user = get_jwt_identity()
        if not is_admin(current_user):
            return {'error': 'Unauthorized action'}, 403
        user_data = api.payload
        try:
            updated_user = facade.update_user(user_id, user_data)
            return {
                'message': 'User updated successfully',
                'data': {
                    'id': updated_user.id,
                    'first_name': updated_user.first_name,
                    'last_name': updated_user.last_name,
                    'email': updated_user.email,
                    'is_admin': updated_user.is_admin
                }
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400

@api.route('/amenities')
class AdminAmenityList(Resource):
    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity created successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new amenity (admin-only)."""
        current_user = get_jwt_identity()
        if not is_admin(current_user):
            return {'error': 'Unauthorized action'}, 403
        amenity_data = api.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return {
                'message': 'Amenity created successfully',
                'data': {
                    'id': new_amenity.id,
                    'name': new_amenity.name
                }
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

@api.route('/places/<place_id>')
class AdminPlaceResource(Resource):
    @jwt_required()
    @api.expect(place_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place (admin-only, bypasses ownership)."""
        current_user = get_jwt_identity()
        if not is_admin(current_user):
            return {'error': 'Unauthorized action'}, 403
        place_data = api.payload
        try:
            updated_place = facade.update_place(place_id, place_data)  # No user_id passed
            return {
                'message': 'Place updated successfully',
                'data': {
                    'id': updated_place.id,
                    'title': updated_place.title,
                    'description': updated_place.description,
                    'price': updated_place.price,
                    'latitude': updated_place.latitude,
                    'longitude': updated_place.longitude,
                    'owner_id': updated_place.owner_id
                }
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400

@api.route('/reviews/<review_id>')
class AdminReviewResource(Resource):
    @jwt_required()
    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review (admin-only, bypasses ownership)."""
        current_user = get_jwt_identity()
        if not is_admin(current_user):
            return {'error': 'Unauthorized action'}, 403
        review_data = api.payload
        try:
            updated_review = facade.update_review(review_id, review_data)  # No user_id passed
            return {
                'message': 'Review updated successfully',
                'data': {
                    'id': updated_review.id,
                    'text': updated_review.text,
                    'rating': updated_review.rating,
                    'user_id': updated_review.user_id,
                    'place_id': updated_review.place_id
                }
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
