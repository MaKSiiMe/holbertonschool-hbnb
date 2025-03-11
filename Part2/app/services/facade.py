#Part2/app/services/facade.py
import logging
#from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class InMemoryRepository:
    def __init__(self):
        self.data = {}
        self.counter = 1

    def add(self, item):
        item.id = self.counter
        self.data[self.counter] = item
        self.counter += 1

    def get(self, item_id):
        return self.data.get(item_id)

    def get_all(self):
        return list(self.data.values())

    def get_by_attribute(self, attribute, value):
        return [item for item in self.data.values() if getattr(item, attribute) == value]

    def update(self, item_id, item_data):
        if item_id in self.data:
            for key, value in item_data.items():
                setattr(self.data[item_id], key, value)

    def delete(self, item_id):
        if item_id in self.data:
            del self.data[item_id]

class Amenity:
    def __init__(self, name):
        self.id = None
        self.name = name

class Place:
    def __init__(self, title, description, price, latitude, longitude, owner):
        self.id = None
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

class Review:
    def __init__(self, text, rating, user, place):
        self.id = None
        self.text = text
        self.rating = rating
        self.user = user
        self.place = place

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # User methods
    def create_user(self, user_data):
        try:
            user = User(
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                email=user_data["email"]
            )
            self.user_repo.add(user)
            return user
        except ValueError as e:
            raise e

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return next((user for user in self.user_repo.get_all() if user.email == email), None)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        self.user_repo.update(user_id, user_data)
        return self.user_repo.get(user_id)

    def delete_user(self, user_id):
        self.user_repo.delete(user_id)
        return self.user_repo.get_all()

    # Amenity methods
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repo.update(amenity_id, amenity_data)
        return self.amenity_repo.get(amenity_id)

    # Place methods
    def create_place(self, place_data):
        owner = self.user_repo.get(place_data["owner_id"])
        if not owner:
            raise ValueError("Owner not found")
        
        if place_data["price"] <= 0:
            raise ValueError("Price must be a positive number")

        place = Place(
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner=owner
        )
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        self.place_repo.update(place_id, place_data)
        return self.place_repo.get(place_id)

    # Review methods
    def create_review(self, review_data):
        try:
            user = self.user_repo.get(review_data["user_id"])
            place = self.place_repo.get(review_data["place_id"])
            
            if not user:
                raise ValueError("User not found")
            if not place:
                raise ValueError("Place not found")

            if not (1 <= review_data["rating"] <= 5):
                raise ValueError("Rating must be between 1 and 5")

            review = Review(
                text=review_data["text"],
                rating=review_data["rating"],
                user=user,
                place=place
            )
            self.review_repo.add(review)
            return review
        except Exception as e:
            logger.error(f"Error creating review: {e}")
            raise e

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return [review for review in self.review_repo.get_all() if review.place.id == place_id]

    def update_review(self, review_id, review_data):
        self.review_repo.update(review_id, review_data)
        return self.review_repo.get(review_id)

    def delete_review(self, review_id):
        self.review_repo.delete(review_id)
        return self.review_repo.get_all()

# Instantiate the HBnBFacade class
facade = HBnBFacade()
