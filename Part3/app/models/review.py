# app/models/review.py

from app.models.BaseModel import BaseModel
from app.extensions import db
from sqlalchemy.orm import relationship


class Review(BaseModel, db.Model):
    """Class representing a Review in the HBnB application."""
    __tablename__ = 'reviews'

    id = db.Column(db.String(36), primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    place = relationship('Place', back_populates='reviews')
    user = relationship('User', back_populates='reviews')

    def __init__(self, text, rating, place_id, user_id):
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

        # Validate text
        if not text or not isinstance(text, str):
            raise ValueError("Review text is required and must be a string")

        # Validate rating
        if not isinstance(rating, int):
            raise ValueError("Rating must be an integer")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")

        # Validation place_id
        if not place_id or not isinstance(place_id, str) or len(place_id) != 36:
            raise ValueError("Invalid place_id")

        # Validation user_id
        if not user_id or not isinstance(user_id, str) or len(user_id) != 36:
            raise ValueError("Invalid user_id")

        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    def update_rating(self, new_rating):
        """
        Update the review rating.

        Args:
            new_rating (int): New rating value (1-5)

        Raises:
            ValueError: If rating is invalid
        """
        if not isinstance(new_rating, int):
            raise ValueError("Rating must be an integer")
        if new_rating < 1 or new_rating > 5:
            raise ValueError("Rating must be between 1 and 5")

        self.rating = new_rating
        self.save()  # Update the updated_at timestamp
