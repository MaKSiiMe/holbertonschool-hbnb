from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

from flask_bcrypt import Bcrypt
from app.persistence.repository import UserRepository, PlaceRepository
from app.persistence.repository import ReviewRepository, AmenityRepository

bcrypt = Bcrypt()


class HBnBFacade:
    """Facade for managing users, places, amenities, and reviews."""

    def __init__(self):
        """Initialize repositories for different models with SQLalchemy"""
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # User Facade
    def create_user(self, user_data):
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve a user by email."""
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        """Update user details with validation."""
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")
        user.update(user_data)
        self.user_repo.save(user)
        return user

    def get_all_users(self):
        """Retrieve all users."""
        return self.user_repo.get_all()

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        if not self.password:
            raise ValueError("Password is not set.")
        if not password:
            raise ValueError("Password is empty.")
        if not self.password.startswith('$2b$'):
            raise ValueError("Invalid password hash.")
        return bcrypt.check_password_hash(self.password, password)

    # Amenity Facade
    def create_amenity(self, amenity_data):
        """Create a new amenity."""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity."""
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")

        amenity.update(amenity_data)
        self.amenity_repo.save(amenity)
        return amenity

    def get_amenity_by_name(self, name):
        """Retrieve an amenity by name."""
        return self.amenity_repo.get_by_attribute('name', name)

    # Place Facade
    def create_place(self, place_data):
        """Create a new place with validation."""
        owner = self.get_user(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found.")
        place = Place(**place_data)
        self.user_repo.add(place)
        return place

    def get_place(self, place_id):
        """Retrieve a place by ID."""
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        return place

    def get_all_places(self):
        """Retrieve all places."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """the function will update a place with new data"""
        place = self.place_repo.get(place_id)
        if not place:
            raise KeyError("Place not found")
        owner = self.get_user(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found.")
        if 'amenities' in place_data:
            amenities = []
            for amenity_id in place_data['amenities']:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raiseValueError(f"Amenity with ID"
                                    "{amenity_id} not found.")
                amenities.append(amenity)
            place.amenities = amenities
        for key, value in place_data.items():
            if hasattr(place, key) and key != 'amenities':
                setattr(place, key, value)

        self.place_repo.save(place)
        return place

    def add_amenity_to_place(self, place_id, amenity_id):
        """ Add an amenity to a place."""
        place = self.get_place(place_id)
        if not place:
            raise ValueError('Place not found')
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError('Amenity not found')
        if amenity in place.amenities:
            return place
        place.amenities.append(amenity)
        self.place_repo.save(place)
        return place

    def delete_amenity_from_place(self, place_id, amenity_id):
        place = self.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}
        if amenity in place.amenities:
            place.amenities.remove(amenity)
            self.place_repo.save(place)
            return place

    # Review Facade
    def create_review(self, review_data):
        """Create a new review."""
        user = self.get_user(review_data['user_id'])
        if not user:
            raise ValueError("User not found.")
        place = self.get_place(review_data['place_id'])
        if not place:
            raise ValueError("Place not found.")
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        return review

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        return [review for review in
                self.review_repo.get_all() if review.place_id == place_id]

    def update_review(self, review_id, review_update):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        for key, value in review_update.items():
            if hasattr(review, key):
                setattr(review, key, value)
        self.review_repo.update(review_id, review.__dict__)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        self.review_repo.delete(review_id)
        return {'message': 'Review deleted succesessfully'}

    def get_review_by_user_and_place(self, user_id, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")
        return [
            review for review in self.review_repo.get_all()
            if review.user_id == user_id and review.place_id == place_id
        ]
