import unittest
from app.models.user import User


class TestUserModel(unittest.TestCase):

    def test_user_creation(self):
        """Test if a User is created with valid attributes."""
        user = User("John", "Doe", "john@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john@example.com")
        self.assertFalse(user.is_admin)

    def test_invalid_email(self):
        """Test that an invalid email raises a ValueError."""
        with self.assertRaises(ValueError):
            User("John", "Doe", "invalid-email")

    def test_add_place(self):
        """Test adding a place to a user."""
        user = User("Alice", "Smith", "alice@example.com")
        place = "Luxury Apartment"
        # Mocked place (normally, this would be a Place object)
        user.add_place(place)
        self.assertIn(place, user.places)

    def test_add_review(self):
        """Test adding a review to a user."""
        user = User("Bob", "Brown", "bob@example.com")
        review = "Excellent stay!"
        # Mocked review (normally, this would be a Review object)
        user.add_review(review)
        self.assertIn(review, user.reviews)


if __name__ == '__main__':
    unittest.main()
