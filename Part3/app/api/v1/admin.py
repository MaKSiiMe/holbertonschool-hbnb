from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity


api = Namespace('admin', description='Admin operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description="User first name", example="John"),
    'last_name': fields.String(required=True, description="User last name", example="Doe"),
    'email': fields.String(required=True, description="User email", example="john@email.com"),
    'password': fields.String(required=True, description="User password", example="Johnd0e!"),
    'is_admin': fields.Boolean(description="User is Admin", example=True)
})

user_update_model = api.model('User Update', {
    'first_name': fields.String(description='First name of the user', example="Jane"),
    'last_name': fields.String(description='Last name of the user', example="Doe"),
    'email': fields.String(description="User email", example="jane@email.com"),
    'password': fields.String(description= "User password", example="janeD0e!"),
    'is_admin': fields.Boolean(description="User is Admin", example=True)
})

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity', example="Wifi")
})

amenity_update_model = api.model('Amenity Update', {
    'name': fields.String(description='Name of the amenity', example="Wi-Fi")
})

place_update_model = api.model('Place Update', {
    'title': fields.String(description='Title of the place', example="Super Apartment"),
    'description': fields.String(description='Description of the place', example="A super place for your week-end!"),
    'price': fields.Float(description='Price per night', example=150.0),
    'latitude': fields.Float(description='Latitude of the place', example=37.7749),
    'longitude': fields.Float(description='Longitude of the place', example=-122.4194),
    'amenities': fields.List(fields.String, description="List of amenities ID's", example=["1fa85f64-5717-4562-b3fc-2c963f66afa6"]),
})

review_update_model = api.model('Review Update', {
    'text': fields.String(description='Text of the review', example="Not so cool!"),
    'rating': fields.Integer(description='Rating of the place (1-5)', example=3),
})


@api.route('/users/')
class AdminUserCreate(Resource):
    @api.expect(user_model)
    @api.response(201, 'User successfully created')
    @api.response(403, 'Admin privileges required')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()

        if not current_user.get('is_admin'):
            api.abort(403, 'Admin privileges required')

        user_data = api.payload

        email = user_data.get('email')

        # Check if email is already in use
        if facade.get_user_by_email(email):
            api.abort(400, 'Email already registered')

        # Logic to create a new user
        try:
            new_user = facade.create_user(user_data)
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))

        return new_user.to_dict(), 201

@api.route('/users/<user_id>')
class AdminUserModify(Resource):
    @api.expect(user_update_model)
    @api.response(201, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(403, 'Admin privileges required')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt_identity()

        if not current_user.get('is_admin'):
            api.abort(403, 'Admin privileges required')
        
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')

        user_data = api.payload

        email = user_data.get('email')

        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                api.abort(400, 'Email already in use')

        try:
            user.update(user_data)
            updated_user = facade.update_user(user_id, user.to_dict())
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))

        return updated_user.to_dict(), 201

@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(403, 'Admin privileges required')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()

        if not current_user.get('is_admin'):
            api.abort(403, 'Admin privileges required')

        amenity_data = api.payload

        # Logic to create a new amenity
        existing_amenity = facade.get_amenity_by_name(amenity_data['name'])
        if existing_amenity:
            api.abort(400, 'Amenity already registered')
        
        try:
            new_amenity = facade.create_amenity(amenity_data)
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))
            
        return new_amenity.to_dict(), 201


@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @api.expect(amenity_update_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def put(self, amenity_id):
        current_user = get_jwt_identity()

        if not current_user.get('is_admin'):
            api.abort(403, 'Admin privileges required')

        amenity_data = api.payload

        # Logic to update an amenity
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        
        existing_amenity = facade.get_amenity_by_name(amenity_data['name'])
        if existing_amenity and existing_amenity.id != amenity.id:
            api.abort(400, "Amenity name already exists")

        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))
        return updated_amenity.to_dict(), 200

@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @api.expect(place_update_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, place_id):
        current_user = get_jwt_identity()

        if not current_user.get('is_admin'):
            api.abort(403, 'Admin privileges required')

        place_data = api.payload

        place = facade.get_place(place_id)

        # Logic to update the place
        if not place:
            api.abort(404, "Place not found")

        if "amenities" in place_data:
            invalid_amenities = []
            for amenity_id in place_data.get("amenities"):
                amenity = facade.get_amenity(amenity_id)
                if not amenity:
                    invalid_amenities.append(amenity_id)
            if invalid_amenities:
                api.abort(400, f"Invalid amenities: {invalid_amenities}")

        try:
            place.update(place_data)
            facade.update_place(place_id, place.to_dict())
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))
        
        return {"message": "Place updated successfully"}, 200

    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def delete(self, place_id):
        current_user = get_jwt_identity()

        if not current_user.get('is_admin'):
            api.abort(403, 'Admin privileges required')

        place = facade.get_place(place_id)
        
        if not place:
            api.abort(404, "Place not found")

        for review_id in place.reviews:
            facade.delete_review(review_id)
        facade.delete_place(place_id)
        return {"message": "Place deleted successfully"}, 200

@api.route('/reviews/<review_id>')
class AdminReviewModify(Resource):
    @api.expect(review_update_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, review_id):
        current_user = get_jwt_identity()

        if not current_user.get('is_admin'):
            api.abort(403, 'Admin privileges required')

        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")

        review_data = api.payload

        # Logic to update the review
        if "user_id" in review_data or "place_id" in review_data:
            api.abort(400, "Invalid input data")

        try:
            review.update(review_data)
            review = review.to_dict()
            del review["id"]
            facade.update_review(review_id, review)
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))

        return {"message": "Review updated successfully"}, 200


    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def delete(self, review_id):
        current_user = get_jwt_identity()

        if not current_user.get('is_admin'):
            api.abort(403, 'Admin privileges required')

        review = facade.get_review(review_id)
        if not review:
            api.abort(404,"Review not found")

        review = review.to_dict()
        place = facade.get_place(review.get("place_id"))

        place.remove_review(review_id)
        facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200