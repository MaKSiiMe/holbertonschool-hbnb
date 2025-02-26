from flask_restx import Namespace, Resource
from app.services.facade import facade

api = Namespace('amenities', description="Amenity operations")

@api.route('/')
class AmenityList(Resource):
    def get(self):
        """Fetch all amenities"""
        return [amenity.to_dict() for amenity in facade.amenity_repo.get_all()]
