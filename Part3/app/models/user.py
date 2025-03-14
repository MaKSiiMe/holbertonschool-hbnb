# app/models/user.py
import re
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.models.BaseModel import BaseModel  
from app.extensions import bcrypt

class User(BaseModel):
    """Class representing a User in the HBnB application."""
    __tablename__ = 'users'  # Table name in the database

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False) # Added password field
    is_admin = Column(Boolean, default=False)

    # Relationships with Place and Review
    places = relationship("Place", back_populates="owner")
    reviews = relationship("Review", back_populates="user")

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        """Initialize a new User instance."""
        super().__init__()

        # Validation (can be moved to a separate function)
        if not first_name or not isinstance(first_name, str) or len(first_name) > 50:
            raise ValueError("Invalid first name")
        if not last_name or not isinstance(last_name, str) or len(last_name) > 50:
            raise ValueError("Invalid last name")
        if not email or not isinstance(email, str) or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError("Invalid email")
        if not isinstance(is_admin, bool):
            raise ValueError("Invalid is_admin")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.hash_password(password) #hash the password on creation

    @property
    def full_name(self):
        """Return the full name of the user."""
        return f"{self.first_name} {self.last_name}"

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

