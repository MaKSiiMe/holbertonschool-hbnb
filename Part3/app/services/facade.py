from app.persistence.repository import UserRepository
from app.persistence.repository import PlaceRepository
from app.persistence.repository import ReviewRepository
from app.persistence.repository import AmenityRepository
from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    def __init__(self):
        self.user_repository = UserRepository()
        self.place_repository = PlaceRepository()
        self.review_repository = ReviewRepository()
        self.amenity_repository = AmenityRepository()

    """
    User
    """

    def create_user(self, user_data):
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repository .add(user)
        return user

    def get_user_by_id(self, user_id):
        return self.user_repository.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repository .get_user_by_email(email)

    def update_user(self, user_id, user_data):
        self.user_repository .update(user_id, user_data)
        return self.user_repository .get(user_id)

    def get_all_users(self):
        users = [
            {'id': 1, 'first_name': 'Jane', 'last_name': 'Doe',
             'email': 'jane.doe@example.com'},
            {'id': 2, 'first_name': 'John', 'last_name': 'Smith',
             'email': 'john.smith@example.com'}
        ]
        return users

    """
    Amenity
    """

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repository .add(amenity)
        return amenity

    def get_amenity_by_name(self, name):
        return self.amenity_repository .get_by_attribute('name', name)

    def get_amenity(self, amenity_id):
        return self.amenity_repository .get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repository .get_all()

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repository .update(amenity_id, amenity_data)
        return self.amenity_repository .get(amenity_id)

    """
    Place
    """

    def create_place(self, place_data):
        place = Place(**place_data)
        self.place_repository .add(place)
        return place

    def get_place(self, place_id):
        return self.place_repository .get(place_id)

    def get_all_places(self):
        return self.place_repository .get_all()

    def update_place(self, place_id, place_data):
        self.place_repository .update(place_id, place_data)
        return self.place_repository .get(place_id)

    """
    Review
    """

    def create_review(self, review_data):
        review = Review(**review_data)
        self.review_repository .add(review)
        return review

    def get_review(self, review_id):
        return self.review_repository .get(review_id)

    def get_all_reviews(self):
        return self.review_repository .get_all()

    def get_reviews_by_place(self, place_id):
        return self.review_repository .get_by_attribute('place_id', place_id)

    def update_review(self, review_id, review_data):
        self.review_repository .update(review_id, review_data)
        return self.review_repository .get(review_id)

    def delete_review(self, review_id):
        self.review_repository .delete(review_id)
        return self.review_repository .get_all()
