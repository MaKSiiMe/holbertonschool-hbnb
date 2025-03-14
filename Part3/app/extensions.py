#app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Centralisation des extensions
db = SQLAlchemy()  # Pour la base de données
bcrypt = Bcrypt()  # Pour le hachage des mots de passe
