# app/models/review.py

from app.models.BaseModel import BaseModel
from app.models.place import Place
from app.models.user import User

class Review(BaseModel):
    """Class representing a Review in the HBnB application."""

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

        # Validate text
        if not text or not isinstance(text, str):
            raise ValueError("Review text is required and must be a string")

        # Validate rating
        if not isinstance(rating, int):
            raise ValueError("Rating must be an integer")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")

        # Validate place
        if not isinstance(place, Place):
            raise ValueError("Place must be a Place instance")

        # Validate user
        if not isinstance(user, User):
            raise ValueError("User must be a User instance")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

        # Add this review to the place's reviews
        place.add_review(self)
        # Add this review to the user's reviews
        user.add_review(self)

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
