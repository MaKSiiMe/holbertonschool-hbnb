#!/usr/bin/python3
''' Amenity Class represents an amenity, inheriting from BaseModel'''


from .basemodel import BaseModel
from sqlalchemy.orm import validates, relationship
from app import db
from app.models.place_amenity import place_amenity


class Amenity(BaseModel):
    '''Represents an amenity with attributes and restrictions'''
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    @validates('name')
    def validate_name(self, key, value):
        '''Validate the name attribute'''
        if not value or len(value) > 50 or not isinstance(value, str):
            raise ValueError(
                "Amenity name must be a string of 1 to 50 characters."
            )
        return value

    def to_dict(self):
        """Convert the Amenity object to a dictionary."""
        return {
            "id": self.id,
            "name": self.name
        }
