from app.models.base_model import BaseModel
from app.models.user import User


class Place(BaseModel):
    """Place class that inherits from BaseModel."""

    def __init__(self, title, description, price, latitude,
                 longitude, owner):
        """
    Constructor for the class, initializing a place or listing with details.

    Args:
        title (str): The title of the place.
        description (str): A description of the place.
        price (float): The price of the place.
        latitude (float): The latitude coordinate of the location.
        longitude (float): The longitude coordinate of the location.
        owner (User): The user who owns the place.
    """
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []