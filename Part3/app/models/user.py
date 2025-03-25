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
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(128), nullable=False) # Added password field
    is_admin = Column(Boolean, default=False)

    # Relationships with Place and Review
    places = relationship("Place", backref="owner", lazy=True)
    reviews = relationship("Review", backref="user", lazy=True)

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        """Initialize a new User instance."""
        super().__init__()

        # Validation (can be moved to a separate function)
        if not first_name or not isinstance(first_name, str) or len(first_name) > 50:
            raise ValueError("First name must be a string (max 50 chars)")

        if not last_name or not isinstance(last_name, str) or len(last_name) > 50:
            raise ValueError("Last name must be a string (max 50 chars)")

        if not email or not isinstance(email, str):
            raise ValueError("Email is required and must be a string")
        
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError("Invalid email format")

        if not isinstance(is_admin, bool):
            raise ValueError("Admin status must be a boolean")
        
        if not password or not isinstance(password, str):
            raise ValueError("Password is required")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.hash_password(password) #hash the password on creation

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
            """Verifies if the provided password matches the hashed password."""
            return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        """Returns a dictionary representation of the User (without password)."""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @property
    def full_name(self):
        """Return the full name of the user."""
        return f"{self.first_name} {self.last_name}"
