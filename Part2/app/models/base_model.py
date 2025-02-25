# app/models/base_model.py

import uuid
from datetime import datetime


class BaseModel:
    """Base class for all models with common attributes and methods."""

    def __init__(self):
        """Initialize a new BaseModel instance with default values."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp whenever the object is modified."""
        self.updated_at = datetime.now()

    def update(self, data):
        """
        Update the attributes of the object based on the provided dictionary.

        Args:
            data (dict): Dictionary containing attribute keys and new values.
        """
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at']:
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp

    def to_dict(self):
        """
        Convert the object to a dictionary representation.

        Returns:
            dict: Dictionary containing all instance attributes.
        """
        obj_dict = self.__dict__.copy()
        # Convert datetime objects to ISO format strings for serialization
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        # Add class name for reference
        obj_dict['__class__'] = self.__class__.__name__
        return obj_dict

    def __str__(self):
        """Return a string representation of the instance."""
        class_name = self.__class__.__name__
        return f"[{class_name}] ({self.id}) {self.__dict__}"
