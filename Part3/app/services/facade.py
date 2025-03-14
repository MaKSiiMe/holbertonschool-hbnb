
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
        db.session.add(user)
        db.session.commit()
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
        db.session.add(amenity)
        db.session.commit()
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
        db.session.add(place)
        db.session.commit()
        return place

    def get_place(self, place_id):
        return self.place_repository.get(place_id)

    def get_all_places(self):
        return self.place_repository.get_all()

    def update_place(self, place_id, place_data):
        self.place_repository.update(place_id, place_data)
        return self.place_repository.get(place_id)

    """
    Place-Amenity Relationship Management
    """
    def add_amenity_to_place(self, place_id, amenity_id):
        """Ajoute une commodité (amenity) à un lieu (place)."""
        from app.models.place import Place
        from app.models.amenity import Amenity

        place = self.get_place(place_id)
        amenity = self.get_amenity(amenity_id)

        if place and amenity:
            place.amenities.append(amenity)
            db.session.commit()
            return place
        return None

    def remove_amenity_from_place(self, place_id, amenity_id):
        """Supprime une commodité (amenity) d'un lieu (place)."""
        from app.models.place import Place
        from app.models.amenity import Amenity

        place = self.get_place(place_id)
        amenity = self.get_amenity(amenity_id)

        if place and amenity and amenity in place.amenities:
            place.amenities.remove(amenity)
            db.session.commit()
            return place
        return None



    """
    Review
    """
    def create_review(self, review_data):
        review = Review(**review_data)
        db.session.add(review)
        db.session.commit()
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
    
    def get_review_by_user_and_place(user_id, place_id):
        """Get a review by user ID and place ID"""
        return Review.query.filter_by(user_id=user_id, place_id=place_id).first()