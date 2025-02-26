from flask_restx import Namespace, Resource
from app.services.facade import facade

api = Namespace('places', description="Place operations")

@api.route('/')
class PlaceList(Resource):
    def get(self):
        """Fetch all places"""
        return [place.to_dict() for place in facade.place_repo.get_all()]
