#app/services/facade.py

from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repository = SQLAlchemyRepository(User)
        self.place_repository = SQLAlchemyRepository(Place)
        self.review_repository = SQLAlchemyRepository(Review)
        self.amenity_repository = SQLAlchemyRepository(Amenity)

    """
    User
    """
    def create_user(self, user_data):
        """Create a new user."""
        user = User(**user_data)
        self.user_repository.add(user)
        return user

    def get_user_by_id(self, user_id):
        return self.user_repository.get(user_id)

    def get_all_users(self):
        return self.user_repository.get_all()

    def get_user_by_email(self, email):
        return self.user_repository.find_by_email(email)

    def update_user(self, user_id, user_data):
        """Update user details, excluding email and password."""
        if 'email' in user_data or 'password' in user_data:
            raise ValueError("You cannot modify email or password.")
        self.user_repository.update(user_id, user_data)
        return self.user_repository.get(user_id)

    def is_admin(self, user_id):
        """Check if a user is an admin."""
        user = self.get_user_by_id(user_id)
        return user.is_admin if user else False

    """
    Amenity
    """
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repository.add(amenity)
        return amenity

    def get_amenity_by_name(self, name):
        return self.amenity_repository.get_by_attribute('name', name)

    def get_amenity(self, amenity_id):
        return self.amenity_repository.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repository.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repository.update(amenity_id, amenity_data)
        return self.amenity_repository.get(amenity_id)

    """
    Place
    """
    def create_place(self, place_data, owner_id=None):
        """Create a new place with ownership validation."""
        if owner_id:
            place_data['owner_id'] = owner_id
        place = Place(**place_data)
        self.place_repository.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repository.get(place_id)

    def get_all_places(self):
        return self.place_repository.get_all()

    def update_place(self, place_id, place_data, user_id=None):
        """Update a place with optional ownership validation."""
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        if user_id and place.owner_id != user_id and not self.is_admin(user_id):
            raise ValueError("Unauthorized action")
        self.place_repository.update(place_id, place_data)
        return self.place_repository.get(place_id)

    """
    Review
    """
    def create_review(self, review_data, user_id=None):
        """Create a new review with ownership and duplicate validation."""
        place_id = review_data['place_id']
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        if user_id and place.owner_id == user_id:
            raise ValueError("You cannot review your own place.")
        existing_review = self.review_repository.get_by_attribute('user_id', user_id)
        if existing_review and existing_review.place_id == place_id:
            raise ValueError("You have already reviewed this place.")
        review_data['user_id'] = user_id
        review = Review(**review_data)
        self.review_repository.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repository.get(review_id)

    def get_all_reviews(self):
        return self.review_repository.get_all()

    def get_reviews_by_place(self, place_id):
        return self.review_repository.get_by_attribute('place_id', place_id)

    def update_review(self, review_id, review_data, user_id=None):
        """Update a review with optional ownership validation."""
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")
        if user_id and review.user_id != user_id and not self.is_admin(user_id):
            raise ValueError("Unauthorized action")
        self.review_repository.update(review_id, review_data)
        return self.review_repository.get(review_id)

    def delete_review(self, review_id, user_id=None):
        """Delete a review with optional ownership validation."""
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")
        if user_id and review.user_id != user_id and not self.is_admin(user_id):
            raise ValueError("Unauthorized action")
        self.review_repository.delete(review_id)
