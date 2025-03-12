from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review', example="Super cool!"),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)', example=5),
    'place_id': fields.String(required=True, description='ID of the place', example="a6e9d55e-c8d1-4268-bb65-4c19a5206a08")
})

review_update_model = api.model('Review Update', {
    'text': fields.String(description='Text of the review', example="Not so cool!"),
    'rating': fields.Integer(description='Rating of the place (1-5)', example=3),
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place', example="Cozy Apartment"),
    'description': fields.String(description='Description of the place', example="A nice place to stay"),
    'price': fields.Float(required=True, description='Price per night', example=100.0),
    'latitude': fields.Float(required=True, description='Latitude of the place', example=37.7749),
    'longitude': fields.Float(required=True, description='Longitude of the place', example=-122.4194),
    'owner_id': fields.String(required=True, description='Owner of the place', example="3fa85f64-5717-4562-b3fc-2c963f66afa6"),
    'amenities': fields.List(fields.String, description="List of amenities ID's", example=["1fa85f64-5717-4562-b3fc-2c963f66afa6"]),
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def post(self):
        """Register a new review"""
        current_user = get_jwt_identity()
        
        review_data = api.payload
        place = facade.get_place(review_data.get("place_id"))
        if not place:
            api.abort(400, "Invalid place")

        user = facade.get_user(current_user.get("id"))
        if not user or user.id == place.owner_id:
            api.abort(403, "Unauthorized action")
        
        review_data["user_id"] = user.id

        place_reviews = facade.get_reviews_by_place(place.id)
        if any(review.user_id == user.id for review in place_reviews):
            api.abort(400, "Place already reviewed")

        try:
            new_review = facade.create_review(review_data)
            place.add_review(new_review.id)
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))

        return {'id': new_review.id, 'place_id': new_review.place_id,
                'rating': new_review.rating, 'text': new_review.text,
                'user_id': new_review.user_id}, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        all_reviews = facade.get_all_reviews()
        return [{'id': review.id, 'place_id': review.place_id,
                 'rating': review.rating, 'text': review.text, 
                 'user_id': review.user_id} for review in all_reviews]

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        
        if not review:
            api.abort(404, 'Review not found')

        return {'id': review.id, 'place_id': review.place_id,
                 'rating': review.rating, 'text': review.text, 
                 'user_id': review.user_id}, 200

    @api.expect(review_update_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        current_user = get_jwt_identity()

        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")

        user = facade.get_user(current_user.get('id'))
        if user.id != review.user_id:
            api.abort(403,'Unauthorized action')

        review_data = api.payload

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
        """Delete a review"""
        current_user = get_jwt_identity()

        review = facade.get_review(review_id)
        if not review:
            api.abort(404,"Review not found")

        user = facade.get_user(current_user.get('id'))
        if user.id != review.user_id:
            api.abort(403,'Unauthorized action')

        review = review.to_dict()
        place = facade.get_place(review.get("place_id"))

        place.remove_review(review_id)
        facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200