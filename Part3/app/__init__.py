from flask import Flask, Blueprint, redirect
from flask_restx import Api
from app.extensions import db, bcrypt, jwt, JWTManager, init_app
from flask_migrate import Migrate
from config import config

#API Namespaces
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.admin import api as admin_ns

jwt = JWTManager()
migrate = Migrate()

def create_app(config_class="development"):
    app = Flask(__name__)
    app.config.from_object(config[config_class])

    # Initialize centralized extensions
    db.init_app(app)
    bcrypt.init_app(app)
    init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Creates the database tables
    #with app.app_context():
        #db.create_all()

    @app.route('/')
    def root():
        return redirect("/api/v1/")
        
    #initialize Blueprint with a root API path
    api_blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
    api = Api(api_blueprint, title='HBnb API', version='1.0', description='HBnB Application API', doc='/')

    # Register namespaces with the API
    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(users_ns, path='/users')
    api.add_namespace(places_ns, path='/places')
    api.add_namespace(amenities_ns, path='/amenities')
    api.add_namespace(reviews_ns, path='/reviews')
    api.add_namespace(admin_ns, path='/admin')
    
    #reigister the blueprint with the app
    app.register_blueprint(api_blueprint)

    return app
