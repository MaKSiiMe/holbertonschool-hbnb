# app/models/amenity.py

from app.models.BaseModel import BaseModel

class Amenity(BaseModel):
    """Class representing an Amenity in the HBnB application."""

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
        if len(name) > 50:
            raise ValueError("Amenity name cannot exceed 50 characters")

        self.name = name
        self.places = []  # List of places that have this amenity

    def add_place(self, place):
        """
        Add a place to the amenity's places and establish
        the bi-directional relationship.

        Args:
            place (Place): Place instance to add
        """
        # Avoid circular import
        from app.models.place import Place

        if not isinstance(place, Place):
            raise ValueError("Place must be a Place instance")

        if place not in self.places:
            self.places.append(place)
            # Add this amenity to the place's amenities if not already present
            if self not in place.amenities:
                place.add_amenity(self)

    def remove_place(self, place):
        """
        Remove a place from the amenity's places.

        Args:
            place (Place): Place instance to remove
        """
        if place in self.places:
            self.places.remove(place)
            # Remove this amenity from the place's amenities if present
            if self in place.amenities:
                place.remove_amenity(self)
