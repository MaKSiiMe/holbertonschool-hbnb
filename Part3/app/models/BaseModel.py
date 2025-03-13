from datetime import datetime
import uuid
from app import db  # Import du module SQLAlchemy

class BaseModel(db.Model):
    """Base model for all other models"""

    __abstract__ = True  # Indique que ce modèle ne sera pas créé en tant que table

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Enregistre ou met à jour l'objet dans la base de données."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Supprime l'objet de la base de données."""
        db.session.delete(self)
        db.session.commit()

    def update(self, data):
        """Mise à jour des attributs avec un dictionnaire de valeurs"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Sauvegarde les modifications
