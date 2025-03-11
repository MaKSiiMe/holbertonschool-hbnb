# app/models/review.py


from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place

class Review(BaseModel):
    """Represents a Review in the HBnB application."""

    def __init__(self, text, rating, user, place):
        """
        Initialize a new Review instance.
        """
        super().__init__()

        # Validate text
        if not text or not isinstance(text, str):
            raise ValueError("Text is required and must be a string")

        # Validate rating (must be between 1 and 5)
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")

        # Validate user
        if not isinstance(user, User):
            raise ValueError("User must be a valid User instance")

        # Validate place
        if not isinstance(place, Place):
            raise ValueError("Place must be a valid Place instance")

        self.text = text
        self.rating = rating
        self.user = user
        self.place = place
