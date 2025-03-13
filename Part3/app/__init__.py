from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns


def create_app(config_class="config.DevelopmentConfig"):
    # Initialisation de l'app Flask avec la configuration
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Configuration de Flask-RESTx
    api = Api(app, 
             version='1.0', 
             title='HBnB API', 
             description='HBnB Application API', 
             doc='/api/v1/')

    # Enregistrement des namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app