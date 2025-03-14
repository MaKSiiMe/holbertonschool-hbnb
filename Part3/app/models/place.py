# app/models/place.py

from app.models.BaseModel import BaseModel
from app.models.user import User


class Place(BaseModel):
    """Class representing a Place in the HBnB application."""

    def __init__(self, title, description, price, latitude, longitude, owner):
        """
        Initialize a new Place instance.

        Args:
            title (str): Title of the place (required, max 100 chars)
            description (str, optional): Description of the place
            price (float): Price per night (must be positive)
            latitude (float): Latitude coordinate (-90 to 90)
            longitude (float): Longitude coordinate (-180 to 180)
            owner (User): User instance of the owner

        Raises:
            ValueError: If any validation fails
        """
        super().__init__()

        # Validate title
        if not title or not isinstance(title, str):
            raise ValueError("Title is required and must be a string")
        if len(title) > 100:
            raise ValueError("Title cannot exceed 100 characters")

        # Validate description (optional)
        if description is not None and not isinstance(description, str):
            raise ValueError("Description must be a string")

        # Validate price
        if not isinstance(price, (int, float)):
            raise ValueError("Price must be a number")
        if price <= 0:
            raise ValueError("Price must be a positive value")

        # Validate latitude
        if not isinstance(latitude, (int, float)):
            raise ValueError("Latitude must be a number")
        if latitude < -90.0 or latitude > 90.0:
            raise ValueError("Latitude must be between -90.0 and 90.0")

        # Validate longitude
        if not isinstance(longitude, (int, float)):
            raise ValueError("Longitude must be a number")
        if longitude < -180.0 or longitude > 180.0:
            raise ValueError("Longitude must be between -180.0 and 180.0")

        # Validate owner
        if not isinstance(owner, User):
            raise ValueError("Owner must be a User instance")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

        # Add this place to the owner's places
        owner.add_place(self)

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def remove_amenity(self, amenity):
        """Remove an amenity from the place."""
        if amenity in self.amenities:
            self.amenities.remove(amenity)

    def get_average_rating(self):
        """
        Calculate the average rating for this place.

        Returns:
            float: Average rating or 0 if no reviews
        """
        if not self.reviews:
            return 0

        total_rating = sum(review.rating for review in self.reviews)
        return total_rating / len(self.reviews)
