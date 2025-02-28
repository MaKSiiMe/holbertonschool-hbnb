from flask import Flask, Blueprint
from flask_restx import Api

def create_app():
    app = Flask(__name__)

    # Initialize blueprint and API
    blueprint = Blueprint('api_v1', __name__)
    api = Api(blueprint, title='HBnB API', version='1.0', description='API for HBnB')

    # Register namespaces
    from .places import api as places_ns
    from .amenities import api as amenities_ns
    from .users import api as users_ns

    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(users_ns, path='/api/v1/users')

    app.register_blueprint(blueprint, url_prefix='/')

    return app
