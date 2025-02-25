from app.persistence.repository import InMemoryRepository
from app.models.user import User


class HBnBFacade:
    def __init__(self):
        """ Initializes a new instance of HBnBFacade.
        Creates an in-memory repository for users.
        """
        self.user_repo = InMemoryRepository()

    def create_user(self, user_data):
        """ Create a new user and add it to the repository."""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """ Retrieves a user by their ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """ Retrieves a user by their email."""
        return self.user_repo.get_by_attribute("email", email)
