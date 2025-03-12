#Part2/app/__init__.py
from flask import Flask, Blueprint, redirect
from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.reviews import api as reviews_ns


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def root():
        return redirect("/api/v1/")
        
    #initialize Blueprint with a root API path
    api_blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
    api = Api(api_blueprint, title='HBnb API', version='1.0', description='HBnB Application API', doc='/')

    # Register namespaces with the API
    api.add_namespace(users_ns, path='/users')
    api.add_namespace(places_ns, path='/places')
    api.add_namespace(amenities_ns, path='/amenities')
    api.add_namespace(reviews_ns, path='/reviews')
    
    #reigister the blueprint with the app
    app.register_blueprint(api_blueprint)

    return app
