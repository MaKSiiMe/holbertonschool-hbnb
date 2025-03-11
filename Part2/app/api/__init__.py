from flask import Blueprint
from flask_restx import Api

# Initialize blueprint and API
blueprint = Blueprint('api', __name__)
api = Api(blueprint, title='HBnB API', version='1.0',
          description='API for HBnB')

# Register namespaces
api.add_namespace(places_ns, path='/api/v1/places')
# Maps /api/v1/places endpoints
# api.add_namespace(amenities_ns, path='/api/v1/amenities')
# api.add_namespace(reviews_ns, path='/api/v1/reviews')
api.add_namespace(users_ns, path='/api/v1/users')

from .v1.places import api as places_ns
api.add_namespace(places_ns, path='/api/v1/places')  # Maps /api/v1/places endpoints