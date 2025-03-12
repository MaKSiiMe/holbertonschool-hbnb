import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.user import User

def test_user_creation():
    try:
        user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == "john.doe@example.com"
        assert user.is_admin == False
        print("User creation test passed.")
    except ValueError as e:
        print(f"User creation test failed: {e}")

def test_invalid_email():
    try:
        user = User(first_name="John", last_name="Doe", email="invalid-email")
    except ValueError as e:
        assert str(e) == "email is not a valid email"
        print("Invalid email test passed.")

if __name__ == "__main__":
    test_user_creation()
    test_invalid_email()