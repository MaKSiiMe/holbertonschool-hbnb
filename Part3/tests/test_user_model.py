import unittest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.user import User
from app.models.BaseModel import BaseModel  # Assurez-vous que le chemin est correct

class TestUserModel(unittest.TestCase):

    def setUp(self):
        # Configuration de la base de données de test en mémoire
        self.engine = create_engine('sqlite:///:memory:')
        BaseModel.metadata.create_all(self.engine)  # Crée les tables
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def tearDown(self):
        self.session.close()
        BaseModel.metadata.drop_all(self.engine)  # Supprime les tables après les tests

    def test_create_user(self):
        # Test de la création d'un utilisateur
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="securePassword"
        )
        self.session.add(user)
        self.session.commit()

        # Vérification que l'utilisateur a été ajouté à la base de données
        retrieved_user = self.session.query(User).filter_by(email="john.doe@example.com").first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.first_name, "John")
        self.assertEqual(retrieved_user.last_name, "Doe")
        self.assertEqual(retrieved_user.email, "john.doe@example.com")
        self.assertTrue(retrieved_user.verify_password("securePassword"))
        self.assertIsInstance(retrieved_user.created_at, datetime)
        self.assertIsInstance(retrieved_user.updated_at, datetime)

    def test_user_password_hashing(self):
        # Test du hachage du mot de passe
        user = User(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            password="anotherPassword"
        )
        self.session.add(user)
        self.session.commit()

        retrieved_user = self.session.query(User).filter_by(email="jane.smith@example.com").first()
        self.assertTrue(retrieved_user.verify_password("anotherPassword"))
        self.assertFalse(retrieved_user.verify_password("wrongPassword"))

    def test_user_full_name(self):
        # Test de la propriété full_name
        user = User(
            first_name="Alice",
            last_name="Wonderland",
            email="alice.wonderland@example.com",
            password="somePassword"
        )
        self.session.add(user)
        self.session.commit()

        self.assertEqual(user.full_name, "Alice Wonderland")

if __name__ == '__main__':
    unittest.main()