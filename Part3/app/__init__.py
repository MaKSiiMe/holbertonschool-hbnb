# app/__init__.py

import os
from flask import Flask, Blueprint, redirect
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from app.extensions import db, bcrypt  # Absolute import for extensions
from config import config  # Ensure this is correct!
# API Namespaces
from app.api.v1.users import api as users_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.places import api as places_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.admin import api as admin_ns  # Import the admin namespace

jwt = JWTManager()
migrate = Migrate()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    # Use the correct config class (string reference)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Define the root route
    @app.route('/')
    def root():
        return redirect("/api/v1/")

    # API Blueprint
    api_blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
    api = Api(api_blueprint, title='HBnB API', version='1.0', description='HBnB Application API', doc='/')

    # Add namespaces to the API
    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(users_ns, path='/users')
    api.add_namespace(places_ns, path='/places')
    api.add_namespace(amenities_ns, path='/amenities')
    api.add_namespace(reviews_ns, path='/reviews')
    api.add_namespace(admin_ns, path='/admin')  # Register the admin namespace

    # Register the API blueprint
    app.register_blueprint(api_blueprint)
    return app
