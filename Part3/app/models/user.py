# app/models/user.py

import re
from app.models.BaseModel import BaseModel

class User(BaseModel):
    """Class representing a User in the HBnB application."""

    def __init__(self, first_name, last_name, email, password, is_admin=False):  # Ajout du password
        
        if not password or not isinstance(password, str):
            raise ValueError("Password is required and must be a string")

        self.hash_password(password)  
        self.password = None  
        self.is_admin = is_admin
        self.places = []
        self.reviews = []

    def hash_password(self, password):
        from app import bcrypt  # Importation locale pour éviter l'importation circulaire
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        from app import bcrypt  # Importation locale pour éviter l'importation circulaire
        return bcrypt.check_password_hash(self.password, password)
