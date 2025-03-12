#Part2/tests/test_user.py
import unittest
from app import create_app
from app.services.facade import HBnBFacade
from app.models.user import User

class TestUserEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create the Flask app and client
        cls.app = create_app()
        cls.client = cls.app.test_client()
        
        # Initialize the facade
        cls.facade = HBnBFacade()

    def setUp(self):
        # Clear the in-memory repository before each test
        self.facade.user_repo._storage.clear()

    def test_create_user_success(self):
        """Test creating a user with valid data."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)
        data = response.json
        self.assertIn("id", data)
        self.assertEqual(data["first_name"], "John")
        self.assertEqual(data["last_name"], "Doe")
        self.assertEqual(data["email"], "john.doe@example.com")

    def test_create_user_invalid_first_name(self):
        """Test creating a user with an empty first name."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)
        self.assertEqual(response.json["error"], "Error creating user: First name is required and must be a string")

    def test_create_user_invalid_email_format(self):
        """Test creating a user with an invalid email format."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)
        self.assertEqual(response.json["error"], "Error creating user: email is not a valid email")

    def test_create_user_duplicate_email(self):
        """Test creating a user with a duplicate email."""
        # Create the first user
        self.facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })

        # Attempt to create another user with the same email
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)
        self.assertEqual(response.json["error"], "Error creating user: email is not a valid email")

    def test_get_all_users(self):
        """Test retrieving all users."""
        # Add two users to the repository
        self.facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        self.facade.create_user({
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })

        # Retrieve all users
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["email"], "john.doe@example.com")
        self.assertEqual(data[1]["email"], "jane.doe@example.com")

    def test_get_user_by_id_success(self):
        """Test retrieving a user by ID."""
        # Create a user
        user = self.facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })

        # Retrieve the user by ID
        response = self.client.get(f'/api/v1/users/{user.id}')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(data["email"], "john.doe@example.com")

    def test_get_user_by_id_not_found(self):
        """Test retrieving a user with an invalid ID."""
        response = self.client.get('/api/v1/users/invalid-id')
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.json)
        self.assertEqual(response.json["error"], "User not found")

    def test_update_user_success(self):
        """Test updating a user's details."""
        # Create a user
        user = self.facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })

        # Update the user's details
        response = self.client.put(f'/api/v1/users/{user.id}', json={
            "first_name": "Jonathan",
            "last_name": "Smith",
            "email": "jonathan.smith@example.com"
        })
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(data["first_name"], "Jonathan")
        self.assertEqual(data["last_name"], "Smith")
        self.assertEqual(data["email"], "jonathan.smith@example.com")

    def test_update_user_invalid_data(self):
        """Test updating a user with invalid data."""
        # Create a user
        user = self.facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })

        # Attempt to update with an invalid email
        response = self.client.put(f'/api/v1/users/{user.id}', json={
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)
        self.assertEqual(response.json["error"], "Error updating user: email is not a valid email")
