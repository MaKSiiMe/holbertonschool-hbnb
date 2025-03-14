from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place management operations')

# ---- Response Models (API Documentation) ----
amenity_model = api.model('Amenity', {
    'id': fields.String(description='Unique amenity ID'),
    'name': fields.String(description='Amenity name (e.g., Wi-Fi)')
})

user_model = api.model('User', {
    'id': fields.String(description='Unique user ID'),
    'first_name': fields.String(description='User first name'),
    'last_name': fields.String(description='User last name'),
    'email': fields.String(description='User email')
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

@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model)
    @api.response(201, 'Place created successfully')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Forbidden')
    def post(self):
        """Create a new Place."""
        try:
            place_data = api.payload
            current_user_id = get_jwt_identity()['id']

            # Validation of the ownership of the place
            if place_data['owner_id'] != current_user_id:
                return {'message': 'You are not authorized to create a place for this owner'}, 403

            new_place = facade.create_place(place_data)
            return new_place.to_dict(), 201
        except ValueError as e:
            return {'message': str(e)}, 400

    @api.response(200, 'Success')
    def get(self):
        """Get all Places"""
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200

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
    @api.response(400, 'Invalid input')
    @api.response(403, 'Forbidden')
    def put(self, place_id):
        """Update a Place (partial updates allowed)."""
        try:
            place_data = api.payload
            current_user_id = get_jwt_identity()['id']

            place = facade.get_place(place_id)
            if not place:
                return {'message': 'Place not found'}, 404

            # Verification of the ownership of the place
            if place.owner_id != current_user_id:
                return {'message': 'You are not authorized to update this place'}, 403

            facade.update_place(place_id, place_data)
            return {'message': 'Place updated successfully'}, 200
        except ValueError as e:
            if 'not found' in str(e):
                return {'message': str(e)}, 404
            return {'message': str(e)}, 400