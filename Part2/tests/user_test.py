import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)
    
    def test_get_users(self):
        """Test to retrieve the list of users"""
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)  
        self.assertIsInstance(response.get_json(), list)  

    def test_user_not_found(self):
        """Test to access a non-existent user"""
        response = self.client.get('/api/v1/users/999')
        self.assertEqual(response.status_code, 404)  

if __name__ == '__main__':
    unittest.main()