from flask_restx import Namespace, Resource
from app.services.facade import facade

api = Namespace('reviews', description="Review operations")

@api.route('/')
class ReviewList(Resource):
    def get(self):
        """Fetch all reviews"""
        return [review.to_dict() for review in facade.review_repo.get_all()]
