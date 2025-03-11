# app/models/user.py


import re
from app.models.base_model import BaseModel

class User(BaseModel):
    """Represents a User in the HBnB application."""

    def __init__(self, first_name, last_name, email):
        """
        Initializes a new User instance.
        """
        super().__init__()

        # Validate first name
        if not first_name or not isinstance(first_name, str):
            raise ValueError("First name is required and must be a string")

        # Validate last name
        if not last_name or not isinstance(last_name, str):
            raise ValueError("Last name is required and must be a string")

        # Validate email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.places = []
        self.reviews = []
        self.is_admin = False

    def add_place(self, place):
        """Adds a place to the user's list of owned places."""
        if place not in self.places:
            self.places.append(place)

    def add_review(self, review):
        """Adds a review to the user's list of reviews."""
        if review not in self.reviews:
            self.reviews.append(review)
