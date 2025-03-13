# app/models/review.py

from app import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.BaseModel import BaseModel

class Review(BaseModel, db.Model):
    """Class representing a Review in the HBnB application."""
    
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    text = Column(String(1000), nullable=False)
    rating = Column(Integer, nullable=False)
    place_id = Column(Integer, ForeignKey('places.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Relations
    place = relationship('Place', back_populates='reviews')
    user = relationship('User', back_populates='reviews')

    def __init__(self, text, rating, place, user):
        """
        Initialize a new Review instance.

        Args:
            text (str): Content of the review (required)
            rating (int): Rating given to the place (1-5)
            place (Place): Place instance being reviewed
            user (User): User instance of the reviewer

        Raises:
            ValueError: If any validation fails
        """
        super().__init__()

        self.set_text(text)
        self.set_rating(rating)

        if not isinstance(place, Place):
            raise ValueError("Place must be a Place instance")
        if not isinstance(user, User):
            raise ValueError("User must be a User instance")

        self.place = place
        self.user = user

    def set_text(self, new_text):
        """Update the review text."""
        if not new_text or not isinstance(new_text, str):
            raise ValueError("Review text is required and must be a string")
        if len(new_text) > 1000:
            raise ValueError("Review text cannot exceed 1000 characters")
        self.text = new_text

    def set_rating(self, new_rating):
        """Update the review rating."""
        if not isinstance(new_rating, int):
            raise ValueError("Rating must be an integer")
        if new_rating < 1 or new_rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        self.rating = new_rating

    def __repr__(self):
        return f"<Review {self.id} - {self.rating} stars>"
