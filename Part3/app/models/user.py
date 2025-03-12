# app/models/user.py

import re
from flask_sqlalchemy import SQLAlchemy
from app.models.BaseModel import BaseModel
from app.extensions import db, bcrypt

class User(BaseModel, db.Model):
    """User model with password hashing and authentication."""

    __tablename__ = 'users'

    id = db.Column(db.String(60), primary_key=True)  # UUID as string
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()

        if not first_name or len(first_name) > 50:
            raise ValueError("First name is required and cannot exceed 50 characters")

        if not last_name or len(last_name) > 50:
            raise ValueError("Last name is required and cannot exceed 50 characters")

        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not email or not re.match(email_pattern, email):
            raise ValueError("Invalid email format")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email.lower()
        self.is_admin = is_admin

        self.set_password(password)

    def set_password(self, password):
        """Hashes the password before storing it."""
        if not password or len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the stored hash."""
        return bcrypt.check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
