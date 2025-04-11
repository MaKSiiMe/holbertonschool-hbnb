#!/usr/bin/python3
'''Base Model module.
This module defines a base class for other models,
providing unique ID generation and timestamp management.
'''


import uuid
from datetime import datetime
from app import db


class BaseModel(db.Model):
    '''Represents a base model with id and timestamp attributes'''
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        '''Update the `updated_at` timestamp to the current time.'''
        self.updated_at = datetime.now()

    def update(self, data):
        '''Update instance attributes based on the given dictionary : data'''
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
