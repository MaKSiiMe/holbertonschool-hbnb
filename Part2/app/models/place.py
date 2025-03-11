# app/models/place.py

from app.models.base_model import BaseModel
from app.models.user import User

class Place(BaseModel):
    """Represents a Place in the HBnB application."""

    def __init__(self, title, description, price, latitude, longitude, owner):
        """
        Initialize a new Place instance.
        """
        super().__init__()

        # Validate title
        if not title or not isinstance(title, str):
            raise ValueError("Title is required and must be a string")
        if len(title) > 100:
            raise ValueError("Title cannot exceed 100 characters")

        # Validate description
        if description is not None and not isinstance(description, str):
            raise ValueError("Description must be a string")

        # Validate price
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Price must be a positive number")

        # Validate latitude
        if not isinstance(latitude, (int, float)) or not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be between -90 and 90")

        # Validate longitude
        if not isinstance(longitude, (int, float)) or not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude must be between -180 and 180")

        # Validate owner
        if not isinstance(owner, User):
            raise ValueError("Owner must be a valid User instance")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.amenities = []  # List of amenities for this place

    def add_amenity(self, amenity):
        """Adds an amenity to the place."""
        if amenity not in self.amenities:
            self.amenities.append(amenity)
