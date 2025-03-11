from flask_restx import Namespace, Resource, fields
from app.services import facade

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
    @api.expect(place_model)
    @api.response(201, 'Place created successfully')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new Place."""
        try:
            new_place = facade.create_place(api.payload)
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

    @api.expect(place_model)
    @api.response(200, 'Place updated')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input')
    def put(self, place_id):
        """Update a Place (partial updates allowed)."""
        try:
            updated_place = facade.update_place(place_id, api.payload)
            return {'message': 'Place updated successfully'}, 200
        except ValueError as e:
            if 'not found' in str(e):
                return {'message': str(e)}, 404
            return {'message': str(e)}, 400
