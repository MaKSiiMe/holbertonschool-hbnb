from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    """Facade layer providing unified interface for HBnB operations"""
    
    def __init__(self):
        # Initialize repositories for all domain entities
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # region User Management
    def create_user(self, user_data):
        """Create new user with automatic password hashing"""
        user = User(**user_data)  # Password is hashed in User constructor
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve user details without password exposure"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Find user by email for authentication purposes"""
        return self.user_repo.find_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        """Update user details with password re-hashing if needed"""
        self.user_repo.update(user_id, user_data)
        return self.user_repo.get(user_id)
    # endregion

    # region Amenity Management
    def create_amenity(self, amenity_data):
        """Add new amenity to the system"""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity_by_name(self, name):
        """Find amenity by its unique name"""
        return self.amenity_repo.find_by_attribute('name', name)

    def get_amenity(self, amenity_id):
        """Retrieve amenity details by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """List all available amenities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Modify existing amenity properties"""
        self.amenity_repo.update(amenity_id, amenity_data)
        return self.amenity_repo.get(amenity_id)
    # endregion

    # region Place Management
    def create_place(self, place_data):
        """Register new rental place"""
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Get place details by ID"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """List all registered places"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update place information"""
        self.place_repo.update(place_id, place_data)
        return self.place_repo.get(place_id)
    # endregion

    # region Review Management
    def create_review(self, review_data):
        """Create new review for a place"""
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Retrieve review details by ID"""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """List all available reviews"""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Find reviews associated with specific place"""
        return self.review_repo.find_by_attribute('place_id', place_id)

    def update_review(self, review_id, review_data):
        """Modify existing review content"""
        self.review_repo.update(review_id, review_data)
        return self.review_repo.get(review_id)

    def delete_review(self, review_id):
        """Remove review from the system"""
        self.review_repo.delete(review_id)
        return self.review_repo.get_all()
