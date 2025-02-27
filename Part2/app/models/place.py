#!/usr/bin/python3
"""This module for the Class Place"""

import uuid
from .base import BaseModel


class Place(BaseModel):
    """To create attibutes for the Class"""
    def __init__(self, title, description, price, latitude, longitude, owner_id, amenities=[]):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenities = amenities  # List to store related amenities
        self.reviews = []  # List to store related reviews

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def remove_review(self, review):
        """Remove a review to the place"""
        self.reviews.remove(review)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value:
            raise TypeError("Title is required")
        if not isinstance(value, str):
            raise TypeError("Title value is not valid")
        if len(value) > 100:
            raise ValueError("Title is too long")
        self._title = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TypeError("Description value is not valid")
        self._description = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not value:
            raise TypeError("Price is required")
        if not isinstance(value, (float, int)):
            raise TypeError("Price value is not valid")
        if value < 0:
            raise ValueError("Price must be a positive number")
        self._price = value

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not value:
            raise TypeError("Latitude is required")
        if not isinstance(value, float):
            raise TypeError("Latitude is not valid")
        if value < -90 or value > 90:
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = value

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not value:
            raise TypeError("Longitude is required")
        if not isinstance(value, float):
            raise TypeError("Longitude is not valid")
        if value < -180 or value > 180:
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = value

    @property
    def owner_id(self):
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value):
        if not value:
            raise TypeError("Owner ID is required")
        if not isinstance(value, str):
            raise TypeError("Owner ID is not valid")
        self._owner_id = value