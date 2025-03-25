<<<<<<< HEAD
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Adding the review model
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
=======
# app/api/v1/places.py

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('places', description='Place management operations')

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(description='Detailed description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Geographic latitude'),
    'longitude': fields.Float(required=True,
                              description='Geographic longitude'),
    'amenities': fields.List(fields.String, required=True,
                             description='List of amenity IDs')
>>>>>>> main
})


@api.route('/')
class PlaceList(Resource):
<<<<<<< HEAD
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload

        user = facade.get_user(place_data.get("owner_id"))
        if not user:
            api.abort(400, "Invalid user")

        invalid_amenities = []
        for amenity_id in place_data.get("amenities"):
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                invalid_amenities.append(amenity_id)
        if invalid_amenities:
            api.abort(400, f"Invalid amenities: {invalid_amenities}")

        try:
            new_place = facade.create_place(place_data)
            user.add_place(new_place.id)
            user_data = user.to_dict()
            facade.update_user(user.id, user_data)
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))

        return {'id': new_place.id, 'title': new_place.title,
                'description': new_place.description, 'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner_id}, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        all_places = facade.get_all_places()
        return [{'id': place.id,
                 'title': place.title,
                 'latitude': place.latitude,
                 'longitude': place.longitude} for place in all_places], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)

        if not place:
            api.abort(404, "Place not found")

        user = facade.get_user(place.owner_id)
        user_data = user.to_dict()
        amenities_data = []
        for amenity_id in place.amenities:
            amenity = facade.get_amenity(amenity_id)
            if amenity:
                amenities_data.append(amenity.to_dict())

        return {'id': place.id, 'title': place.title,
                'description': place.description, 'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude, 'owner': user_data,
                'amenities': amenities_data}, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload

        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")
        if place_data.get("owner_id") != place.owner_id:
            api.abort(400, "Owner can not be modified")
        if place_data.get("latitude") != place.latitude or place_data.get("longitude") != place.longitude:
            api.abort(400, "Latitude and Longitude can not been modified")
        invalid_amenities = []
        for amenity_id in place_data.get("amenities"):
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                invalid_amenities.append(amenity_id)
        if invalid_amenities:
            api.abort(400, f"Invalid amenities: {invalid_amenities}")

        try:
            facade.update_place(place_id, place_data)
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))

        return {"message": "Place updated successfully"}, 200
=======
    @jwt_required()
    @api.expect(place_model)
    @api.response(201, 'Place created successfully')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new Place."""
        current_user = get_jwt_identity()
        try:
            place_data = api.payload
            place_data['owner_id'] = current_user
            new_place = facade.create_place(place_data)
            return new_place.to_dict(), 201
        except ValueError as e:
            return {'message': str(e)}, 400

    @api.response(200, 'Success')
    def get(self):
        """Get all Places (summary)."""
        places = facade.get_all_places()
        return [place.to_summary_dict() for place in places], 200


@api.route('/<string:place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Success')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get full details of a Place."""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, 'Place not found')
        return place.to_detail_dict(), 200

    @jwt_required()
    @api.expect(place_model)
    @api.response(200, 'Place updated')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input')
    def put(self, place_id):
        """Update a Place (partial updates allowed)."""
        current_user = get_jwt()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')
        try:
            place = facade.get_place(place_id)
            if not place:
                return {'message': 'Place not found'}, 404
            if not is_admin and place.owner_id != user_id:
                return {'error': 'Unauthorized action'}, 403
            updated_place = facade.update_place(place_id, api.payload,
                                                user_id=user_id)
            return {'message': 'Place updated successfully'}, 200
        except ValueError as e:
            return {'message': str(e)}, 400
>>>>>>> main
