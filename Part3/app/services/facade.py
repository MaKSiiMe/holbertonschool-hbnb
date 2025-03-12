
from app.persistence.repository import SQLAlchemyRepository
from app.models import User, Place, Review, Amenity
from app.extensions import db

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
        self.user_repository.update(user_id, user_data)
        return self.user_repository.get(user_id)

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
    def create_place(self, place_data):
        place = Place(**place_data)
        self.place_repository.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repository.get(place_id)

    def get_all_places(self):
        return self.place_repository.get_all()

    def update_place(self, place_id, place_data):
        self.place_repository.update(place_id, place_data)
        return self.place_repository.get(place_id)

    """
    Review
    """
    def create_review(self, review_data):
        review = Review(**review_data)
        self.review_repository.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repository.get(review_id)

    def get_all_reviews(self):
        return self.review_repository.get_all()

    def get_reviews_by_place(self, place_id):
        return self.review_repository.get_by_attribute('place_id', place_id)

    def update_review(self, review_id, review_data):
        self.review_repository.update(review_id, review_data)
        return self.review_repository.get(review_id)

    def delete_review(self, review_id):
        self.review_repository.delete(review_id)
        return self.review_repository.get_all()