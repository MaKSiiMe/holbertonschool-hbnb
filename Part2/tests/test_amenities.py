#Part2/tests//test_amenities.py


import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_create_valid_amenity(client):
    response = client.post('/api/v1/amenities/', json={"name": "Wi-Fi"})
    assert response.status_code == 201
    assert "id" in response.json

def test_create_amenity_invalid_data(client):
    response = client.post('/api/v1/amenities/', json={"name": ""})
    assert response.status_code == 400
    assert response.json["error"] == "Amenity name cannot be empty"

def test_get_non_existent_amenity(client):
    response = client.get('/api/v1/amenities/99999')
    assert response.status_code == 404
    assert response.json["error"] == "Amenity not found"
