# app/models/amenity.py
from app.models.BaseModel import BaseModel
from app.extensions import db
from sqlalchemy.orm import relationship

# Association table for the Many-to-Many relationship
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Amenity(BaseModel, db.Model):
    """Class representing an Amenity in the HBnB application."""
    __tablename__ = 'amenities'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    places = relationship('Place', secondary=place_amenity, back_populates='amenities')

    def __init__(self, name):
        """
        Initialize a new Amenity instance.

        Args:
            name (str): Name of the amenity (required, max 50 chars)

        Raises:
            ValueError: If name validation fails
        """
        super().__init__()

        # Validate name
        if not name or not isinstance(name, str):
            raise ValueError("Amenity name is required and must be a string")
        if len(name) > 128:
            raise ValueError("Amenity name cannot exceed 128 characters")

        self.name = name
 