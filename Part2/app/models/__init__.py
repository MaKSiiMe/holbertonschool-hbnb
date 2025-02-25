# app/models/__init__.py

# Import all model classes to make them accessible when importing from models
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

# To support importing BaseModel if needed
# This assumes BaseModel is in a base_model.py file
from app.models.base_model import BaseModel

# Define what's available when someone does `from app.models import *`
__all__ = ['BaseModel', 'User', 'Place', 'Review', 'Amenity']

# You could also include a version number for your models package
__version__ = '0.1.0'
