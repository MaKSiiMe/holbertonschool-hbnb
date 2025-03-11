# filepath: /home/gioarias/holbertonschool-HBnB/Part2/app/api/v1/__init__.py
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns  # Import the reviews namespace

api = Api(title="HBnB API", version="1.0")
api.add_namespace(users_ns, path='/users')
api.add_namespace(amenities_ns, path='/amenities')
api.add_namespace(places_ns, path='/places')
api.add_namespace(reviews_ns, path='/reviews')  # Register the reviews namespace
