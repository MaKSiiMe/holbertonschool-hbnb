# app/models/user.py


import re
from app.models.base_model import BaseModel


class User(BaseModel):
    """Represents a User in the HBnB application."""

    def __init__(self, first_name, last_name, email, is_admin=False):
        """
        Initializes a new User instance.

        Args:
            first_name (str): User's first name (max 50 chars).
            last_name (str): User's last name (max 50 chars).
            email (str): User's unique email.
            is_admin (bool): Whether the user is an admin (default False).

        Raises:
            ValueError: If input validation fails.
        """
        super().__init__()

        # Validate first name
        if not first_name or not isinstance(first_name, str):
            raise ValueError("First name is required and must be a string")
        if len(first_name) > 50:
            raise ValueError("First name cannot exceed 50 characters")

        # Validate last name
        if not last_name or not isinstance(last_name, str):
            raise ValueError("Last name is required and must be a string")
        if len(last_name) > 50:
            raise ValueError("Last name cannot exceed 50 characters")

        # Validate email
        if not email or not isinstance(email, str):
            raise ValueError("Email is required and must be a string")

        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValueError(f"Invalid email format: {email}")

        # Validate is_admin
        if not isinstance(is_admin, bool):
            raise ValueError("is_admin must be a boolean value")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []  # Stores owned places
        self.reviews = []  # Stores user reviews

    def add_place(self, place):
        """Adds a place to the user's list of owned places."""
        if place not in self.places:
            self.places.append(place)

    def add_review(self, review):
        """Adds a review to the user's list of written reviews."""
        if review not in self.reviews:
            self.reviews.append(review)

    @property
    def full_name(self):
        """
        Returns the full name of the user.

        Returns:
            str: Full name (first_name + last_name)
        """
        return f"{self.first_name} {self.last_name}"
