#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity', example="Wifi")
})

amenity_update_model = api.model('Amenity Update', {
    'name': fields.String(description='Name of the amenity', example="Wi-Fi")
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload

        existing_amenity = facade.get_amenity_by_name(amenity_data['name'])
        if existing_amenity:
            api.abort(400, 'Amenity already registered')
        
        try:
            new_amenity = facade.create_amenity(amenity_data)
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))
            
        return new_amenity.to_dict(), 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        all_amenities = facade.get_all_amenities()
        return [{'id': amenity.id, 'name': amenity.name} for amenity in all_amenities]

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, 'Amenity not found')

        return amenity.to_dict(), 200
    
    
    @api.expect(amenity_update_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = api.payload

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