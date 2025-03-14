# app/models/user.py

import re
from app.models.BaseModel import BaseModel
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(BaseModel):
    """Class representing a User in the HBnB application."""
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        """
        Initialize a new User instance.
        Args:
            first_name (str): First name of the user (required, max 50 chars)
            last_name (str): Last name of the user (required, max 50 chars)
            email (str): Email address of the user (required, must be valid format)
            password (str): Password of the user (required, will be hashed)
            is_admin (bool, optional): Admin status. Defaults to False.
        Raises:
            ValueError: If any validation fails
        """
        super().__init__()
        # Validate first_name
        if not first_name or not isinstance(first_name, str):
            raise ValueError("First name is required and must be a string")
        if len(first_name) > 50:
            raise ValueError("First name cannot exceed 50 characters")
        # Validate last_name
        if not last_name or not isinstance(last_name, str):
            raise ValueError("Last name is required and must be a string")
        if len(last_name) > 50:
            raise ValueError("Last name cannot exceed 50 characters")
        # Validate email
        if not email or not isinstance(email, str):
            raise ValueError("Email is required and must be a string")
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValueError("email is not a valid email")
        # Validate password
        if not password or not isinstance(password, str):
            raise ValueError("Password is required and must be a string")
        # Validate is_admin
        if not isinstance(is_admin, bool):
            raise ValueError("is_admin must be a boolean value")
        
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.password = None  # Placeholder for hashed password
        self.hash_password(password)  # Hash the password during initialization
        self.places = []  # List to store places owned by the user
        self.reviews = []  # List to store reviews written by the user

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def add_place(self, place):
        """Add a place to the user's owned places."""
        self.places.append(place)

    def add_review(self, review):
        """Add a review to the user's written reviews."""
        self.reviews.append(review)

    @property
    def full_name(self):
        """
        Return the full name of the user.
        Returns:
            str: Full name (first_name + last_name)
        """
        return f"{self.first_name} {self.last_name}"

    def to_dict(self):
        """
        Convert the User instance to a dictionary excluding sensitive fields.
        Returns:
            dict: Dictionary representation of the user.
        """
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        }
