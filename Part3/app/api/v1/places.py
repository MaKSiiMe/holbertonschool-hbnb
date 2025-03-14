#app/api/v1/places.py

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('places', description='Place management operations')

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(description='Detailed description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Geographic latitude'),
    'longitude': fields.Float(required=True, description='Geographic longitude'),
    'amenities': fields.List(fields.String, required=True, description='List of amenity IDs')
})

@api.route('/')
class PlaceList(Resource):
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
            updated_place = facade.update_place(place_id, api.payload, user_id=user_id)
            return {'message': 'Place updated successfully'}, 200
        except ValueError as e:
            return {'message': str(e)}, 400
