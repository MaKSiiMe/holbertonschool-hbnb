from app.persistence.repository import InMemoryRepository
from app import db

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    """
    User
    """
    def create_user(self, user_data):
        from app.models.user import User
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        return user

    def get_user(self, user_id):
        from app.models.user import User
        return User.query.get(user_id)

    def get_user_by_email(self, email):
        from app.models.user import User
        return User.query.filter_by(email=email).first()

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if user:
            for key, value in user_data.items():
                setattr(user, key, value)
            db.session.commit()
        return user

    """
    Amenity
    """
    def create_amenity(self, amenity_data):
        from app.models.amenity import Amenity
        amenity = Amenity(**amenity_data)
        db.session.add(amenity)
        db.session.commit()
        return amenity

    def get_amenity(self, amenity_id):
        from app.models.amenity import Amenity
        return Amenity.query.get(amenity_id)

    def get_all_amenities(self):
        from app.models.amenity import Amenity
        return Amenity.query.all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if amenity:
            for key, value in amenity_data.items():
                setattr(amenity, key, value)
            db.session.commit()
        return amenity

    """
    Place
    """
    def create_place(self, place_data):
        from app.models.place import Place
        place = Place(**place_data)
        db.session.add(place)
        db.session.commit()
        return place

    def get_place(self, place_id):
        from app.models.place import Place
        return Place.query.get(place_id)

    def get_all_places(self):
        from app.models.place import Place
        return Place.query.all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if place:
            for key, value in place_data.items():
                setattr(place, key, value)
            db.session.commit()
        return place

    """
    Gestion de la relation Place-Amenity
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
        from app.models.review import Review
        review = Review(**review_data)
        db.session.add(review)
        db.session.commit()
        return review

    def get_review(self, review_id):
        from app.models.review import Review
        return Review.query.get(review_id)

    def get_all_reviews(self):
        from app.models.review import Review
        return Review.query.all()

    def get_reviews_by_place(self, place_id):
        from app.models.review import Review
        return Review.query.filter_by(place_id=place_id).all()

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if review:
            for key, value in review_data.items():
                setattr(review, key, value)
            db.session.commit()
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if review:
            db.session.delete(review)
            db.session.commit()
