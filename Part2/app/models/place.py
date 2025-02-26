class Place:
    """Represents a place with validated attributes."""
    def __init__(self, title, description, price, latitude, longitude, owner_id, amenities=None):
        self.title = title
        self.description = description
        self.price = price  # Uses the price setter for validation
        self.latitude = latitude  # Uses the latitude setter
        self.longitude = longitude  # Uses the longitude setter
        self.owner_id = owner_id
        self.amenities = amenities if amenities else []

    # ---- Property Validations ----
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        """Validates that price is a non-negative float."""
        if value < 0:
            raise ValueError("Price must be a non-negative number.")
        self._price = value

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        """Validates latitude is between -90 and 90."""
        if not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        self._latitude = value

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        """Validates longitude is between -180 and 180."""
        if not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180.")
        self._longitude = value