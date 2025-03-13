# app/models/place.py

from app import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, CheckConstraint
from sqlalchemy.orm import relationship, validates

# Table d'association many-to-many pour les commodités
place_amenity = db.Table(
    'place_amenity',
    Column('place_id', Integer, ForeignKey('places.id'), primary_key=True),
    Column('amenity_id', Integer, ForeignKey('amenities.id'), primary_key=True)
)

class Place(db.Model):
    __tablename__ = 'places'
    __table_args__ = (
        CheckConstraint('price > 0', name='check_price_positive'),
        CheckConstraint('latitude BETWEEN -90 AND 90', name='check_latitude_range'),
        CheckConstraint('longitude BETWEEN -180 AND 180', name='check_longitude_range'),
    )

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    price = Column(Float, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Relations
    user = relationship('User', backref='places')
    reviews = relationship('Review', backref='place', cascade='all, delete-orphan', lazy='dynamic')
    amenities = relationship('Amenity', secondary=place_amenity, backref='places')

    @validates('title')
    def validate_title(self, key, title):
        if not title or len(title) > 100:
            raise ValueError("Le titre doit être une chaîne de 1 à 100 caractères")
        return title

    @validates('price')
    def validate_price(self, key, price):
        if price <= 0:
            raise ValueError("Le prix doit être positif")
        return price

    def get_average_rating(self):
        """Calcule la note moyenne des avis associés à ce lieu."""
        if self.reviews.count() == 0:
            return 0.0
        return round(
            sum(review.rating for review in self.reviews) / self.reviews.count(), 
            2
        )

    def add_review(self, review):
        """Ajoute un avis au lieu."""
        if review not in self.reviews:
            self.reviews.append(review)
            db.session.commit()

    def add_amenity(self, amenity):
        """Ajoute une commodité au lieu."""
        if amenity not in self.amenities:
            self.amenities.append(amenity)
            db.session.commit()

    def __repr__(self):
        return f"<Place {self.title} (ID: {self.id})>"
