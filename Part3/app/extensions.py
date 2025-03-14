from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Centralisation des extensions
db = SQLAlchemy()  # Pour la base de données
bcrypt = Bcrypt() # Pour le hachage des mots de passe
jwt = JWTManager()

def init_app(app):
    jwt.init_app(app)