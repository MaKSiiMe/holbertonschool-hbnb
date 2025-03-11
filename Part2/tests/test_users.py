#Part2/tests/test_user.py


import pytest
from app import create_app
from app.api.v1.users import api
from flask_restx import Resource

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_create_valid_user(client):
    response = client.post('/api/v1/users/', json={
        "first_name": "Alice",
        "last_name": "Doe",
        "email": "alice@example.com"
    })
    assert response.status_code == 201
    assert "id" in response.json

def test_create_user_invalid_email(client):
    response = client.post('/api/v1/users/', json={
        "first_name": "Alice",
        "last_name": "Doe",
        "email": "invalid-email"
    })
    assert response.status_code == 400
    assert "Invalid email format" in response.json["error"]

def test_get_non_existent_user(client):
    response = client.get('/api/v1/users/99999')
    assert response.status_code == 404
    assert response.json["error"] == "User not found"
