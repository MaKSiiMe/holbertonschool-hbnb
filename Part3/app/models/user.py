#!/usr/bin/python3
"""This module for the Class User"""

from app import bcrypt, db
import uuid
from .base import BaseModel
from sqlalchemy.orm import validates
from sqlalchemy import func
import re


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    

    def add_place(self, place):
        """This function to add places"""
        self.places.append(place)
        
    def update(self, data):
        if "first_name" in data:
            self.first_name = data["first_name"]
        if "last_name" in data:
            self.last_name = data["last_name"]
        if "email" in data:
            self.email = data["email"]

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
        }
        
    def hash_password(self, password):
        """Hashes the password before storing it."""
        pattern = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$")
        if not isinstance(password, str):
            raise TypeError("Password must be a string")
        if not password:
            raise TypeError("Password is required")
        mat = re.search(pattern, password)
        if not mat:
            raise ValueError("Password must have at least: 8 characters with 1 lowercase, 1 uppercase, 1 number and 1 special character")
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
    
    @validates('first_name', 'last_name')
    def validate_first_name(self, key, value):
        if not isinstance(value, str):
            raise TypeError("{} must be a string".format(key.replace("_", " ")).capitalize())
        if len(value.replace(" ", "")) < 2 or len(value.replace(" ", "")) > 50:
            raise ValueError("{} must have between 2 and 50 characters".format(key.replace("_", " ")).capitalize())
        return value

    @validates('email')
    def validate_email(self, key, value):
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        if not value:
            raise TypeError("Email is required")
        if not re.match(
            r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{2,}$", value
        ):
            raise ValueError("Email is not valid")
        existing_user = User.query.filter(value.lower() == func.lower(User.email)).first()
        if existing_user:
            raise ValueError("Email already registered")
        return value

    @validates('is_admin')
    def validate_is_admin(self, key, value):
        if not isinstance(value, bool):
            raise TypeError("Admin must be True or False")
        return value