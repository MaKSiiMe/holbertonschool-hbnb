# app/models/amenity.py

from app import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.BaseModel import BaseModel
from app.models.place_amenity import place_amenity

class Amenity(BaseModel, db.Model):
    """Class representing an Amenity in the HBnB application."""

    __tablename__ = 'amenities'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    # Relation plusieurs-à-plusieurs avec Place
    places = relationship('Place', secondary=place_amenity, back_populates='amenities')
