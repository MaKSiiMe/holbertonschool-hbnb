#Part2/tests/test_places.py
import pytest
from app import create_app
from app.api.v1.places import api
from flask_restx import Resource

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_create_valid_place(client):
    # First create valid user
    user_resp = client.post('/api/v1/users/', json={
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com"
    })
    assert user_resp.status_code == 201
    owner_id = user_resp.json["id"]
    
    place_resp = client.post('/api/v1/places/', json={
        "title": "Cozy Cabin",
        "price": 100,
        "latitude": 40.7128,
        "longitude": -74.0060,
        "owner_id": owner_id
    })
    assert place_resp.status_code == 201
    assert "id" in place_resp.json

def test_create_place_invalid_price(client):
    user_resp = client.post('/api/v1/users/', json={
        "first_name": "Alice",
        "last_name": "Doe",
        "email": "alice@example.com"
    })
    assert user_resp.status_code == 201
    owner_id = user_resp.json["id"]

    response = client.post('/api/v1/places/', json={
        "title": "Beach House",
        "description": "A beautiful beach house",
        "price": -50,  # Invalid price
        "latitude": 34.05,
        "longitude": -118.25,
        "owner_id": owner_id
    })
    assert response.status_code == 400
    assert response.json["error"] == "Price must be a positive number"

def test_get_non_existent_place(client):
    response = client.get('/api/v1/places/99999')
    assert response.status_code == 404
    assert response.json["error"] == "Place not found"
