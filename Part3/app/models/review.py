
#!/usr/bin/python3
"""This module for the Class Review"""


from .base import BaseModel


class Review(BaseModel):
    """To create attibutes for the Class"""
    def __init__(self, place_id, user_id, rating, text):
        super().__init__()
        self.place_id = place_id
        self.user_id = user_id
        self.rating = rating
        self.text = text

    def update(self, data):
        if 'text' in data:
            self.text = data['text']
        if 'rating' in data:
            self.rating = data['rating']

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            raise TypeError("Text is not valid")
        if not value:
            raise TypeError("Text is required")
        self._text = value

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not value:
            raise TypeError("Rating is required")
        if not isinstance(value, int):
            raise TypeError("Rating is not valid")
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5")
        self._rating = value

    @property
    def place_id(self):
        return self._place_id

    @place_id.setter
    def place_id(self, value):
        if not value:
            raise TypeError("Place is required")
        if not isinstance(value, str):
            raise TypeError("Place is not valid")
        self._place_id = value

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        if not value:
            raise TypeError("User is required")
        if not isinstance(value, str):
            raise TypeError("User is not valid")
        self._user_id = value
    
    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id
        }
