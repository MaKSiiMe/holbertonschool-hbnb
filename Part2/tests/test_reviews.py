#Part2/tests/test_reviews.py


import pytest
from app import create_app
from app.api.v1.reviews import api
from flask_restx import Resource

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_create_valid_review(client):
    # Create a user
    user_response = client.post('/api/v1/users/', json={
        "first_name": "Bob",
        "last_name": "Smith",
        "email": "bob@example.com"
    })
    assert user_response.status_code == 201
    user_id = user_response.json["id"]
    
    # Create a place
    place_response = client.post('/api/v1/places/', json={
        "title": "Mountain Cabin",
        "description": "A cozy cabin in the mountains",
        "price": 150,
        "latitude": 40.7128,
        "longitude": -74.0060,
        "owner_id": user_id
    })
    assert place_response.status_code == 201
    place_id = place_response.json["id"]
    
    # Create a review
    response = client.post('/api/v1/reviews/', json={
        "text": "Great place!",
        "rating": 5,
        "user_id": user_id,
        "place_id": place_id
    })
    assert response.status_code == 201
    assert "id" in response.json

def test_create_review_invalid_rating(client):
    response = client.post('/api/v1/reviews/', json={
        "text": "Bad experience.",
        "rating": 10,  # Invalid rating
        "user_id": "random-id",
        "place_id": "random-id"
    })
    assert response.status_code == 400
    assert response.json["error"] == "Rating must be between 1 and 5"

def test_get_non_existent_review(client):
    response = client.get('/api/v1/reviews/99999')
    assert response.status_code == 404
    assert response.json["error"] == "Review not found"
