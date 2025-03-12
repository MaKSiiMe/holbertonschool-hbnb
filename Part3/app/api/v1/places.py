from flask import jsonify
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

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
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

place_update_model = api.model('Place Update', {
    'title': fields.String(description='Title of the place', example="Super Apartment"),
    'description': fields.String(description='Description of the place', example="A super place for your week-end!"),
    'price': fields.Float(description='Price per night', example=150.0),
    'latitude': fields.Float(description='Latitude of the place', example=37.7749),
    'longitude': fields.Float(description='Longitude of the place', example=-122.4194),
    'amenities': fields.List(fields.String, description="List of amenities ID's", example=["1fa85f64-5717-4562-b3fc-2c963f66afa6"]),
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def post(self):
        """Register a new place"""
        current_user = get_jwt_identity()

        user = facade.get_user(current_user.get("id"))
        if not current_user:
            api.abort(403, "Unauthorized action")

        place_data = api.payload

        place_data["owner_id"] = user.id

        amenities_ids = place_data.get("amenities")
        if amenities_ids:
            invalid_amenities = [amenity_id for amenity_id in amenities_ids if not facade.get_amenity(amenity_id)]
            if invalid_amenities:
                api.abort(400, f"Invalid amenities: {invalid_amenities}")

        try:    
            new_place = facade.create_place(place_data)
            user.add_place(new_place.id)
            user_data = user.to_dict()
            facade.update_user(user.id, user_data)
            new_place_data = new_place.to_dict()
            del new_place_data["amenities"]
            del new_place_data["reviews"]
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))

        return new_place_data, 201

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
        
        reviews_data = []
        for review_id in place.reviews:
            review = facade.get_review(review_id)
            if review:
                review_data = review.to_dict()
                del review_data['place_id']
                reviews_data.append(review_data)
            

        return {'id': place.id, 'title': place.title,
                'descripton': place.description, 'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude, 'owner': user_data,
                'amenities': amenities_data,
                'reviews': reviews_data}, 200

    @api.expect(place_update_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        current_user = get_jwt_identity()

        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")

        if place.owner_id != current_user.get('id'):
            api.abort(403,'Unauthorized action')

        place_data = api.payload
        
        if "owner_id" in place_data:
            api.abort(400, 'Invalid input data')

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

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)

        if not place:
            api.abort(404, 'Place not found')
        
        reviews = facade.get_reviews_by_place(place.id)
        place_reviews = [
            {key: value for key, value in review.to_dict().items() if key not in ["user_id", "place_id"]}
            for review in reviews
        ]

        return place_reviews, 200